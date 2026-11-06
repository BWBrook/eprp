import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import elsevier as e
import mine_elsevier as m


CELL = "10.1016/j.cell.2016.07.021"
LOPEZ = "10.1016/j.tree.2015.09.005"
ABDELHADY = "10.1016/j.jafrearsci.2023.105155"
FILLER = "Synthetic fixture content describes an invented research context without source quotations. " * 4


def article(doi, body):
    return (f'<full-text-retrieval-response xmlns:p="urn:prism"><coredata><p:doi>{doi}</p:doi>'
            f'</coredata><originalText><body>{body}</body></originalText>'
            '</full-text-retrieval-response>').encode()


def cell():
    sections = []
    for i, ((name, _, _), count) in enumerate(zip(m.CELL_THEMES, [3, 1, 3, 2, 2, 4]), 1):
        sections.append(f'<section id="sec1.{i}"><section-title>Synthetic heading</section-title>'
                        f'<para id="b{i}">{name}, synthetic affiliation</para>'
                        f'<para id="p{i}">{FILLER}' + "Synthetic question? " * count + '</para></section>')
    return article(CELL, '<section id="sec1"><section-title>Synthetic container</section-title>'
                   + ''.join(sections) + '</section>')


def lopez():
    return article(LOPEZ, '<textbox id="tb0005"><label>Synthetic box</label><textbox-body>'
                   '<sections>' + ''.join(f'<para id="par{95 + i * 5:04d}">{FILLER}'
                   + 'Synthetic question? ' * count + '</para>'
                   for i, count in enumerate([2, 3, 4, 2, 1, 3, 3, 1]))
                   + '</sections></textbox-body></textbox>')


def abdelhady():
    return article(ABDELHADY, ''.join(f'<section id="{sid}"><section-title>Synthetic heading</section-title>'
                   f'<para id="context{i}">{FILLER}' + 'Synthetic question? ' * 3 + '</para></section>'
                   for i, sid in enumerate(['sec1', 'sec4.5'], 1)))


class CurationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Path(self.temp.name) / 'overlay'
        self.reviewed = {CELL: e.sha(cell()), LOPEZ: e.sha(lopez()), ABDELHADY: e.sha(abdelhady())}
        self.hash_patch = patch.object(m, 'REVIEWED_XML_SHA256', self.reviewed)
        self.hash_patch.start()
        with e.locked(self.store) as root:
            self.root = root
            for wid, doi, data in [('W1', CELL, cell()), ('W2', LOPEZ, lopez()),
                                   ('W3', ABDELHADY, abdelhady())]:
                text = e.parse_article(data, doi)[0].encode()
                e.atomic(root / 'xml' / (wid + '.xml'), data)
                e.atomic(root / 'text' / (wid + '.txt'), text)
                e.append(root / 'manifest.tsv', {'openalex_id': wid, 'doi': doi,
                         'xml_path': f'xml/{wid}.xml', 'text_path': f'text/{wid}.txt',
                         'xml_sha256': e.sha(data), 'text_sha256': e.sha(text)}, e.FIELDS)

    def tearDown(self):
        self.hash_patch.stop()
        self.temp.cleanup()

    def private(self):
        return json.loads((self.root / 'derived/agenda-curated-units.json').read_text())

    def replace_source(self, wid, doi, data):
        rows = e.latest(self.root / 'manifest.tsv')
        row = rows[wid]
        text = e.parse_article(data, doi)[0].encode()
        e.atomic(self.root / row['xml_path'], data)
        e.atomic(self.root / row['text_path'], text)
        row.update(xml_sha256=e.sha(data), text_sha256=e.sha(text))
        e.append(self.root / 'manifest.tsv', row, e.FIELDS)
        self.reviewed[doi] = e.sha(data)

    def test_curated_units_have_private_wording_and_safe_summary(self):
        summary = m.curate(self.store)
        sources = self.private()['sources']
        self.assertEqual([len(sources[d]['units']) for d in [CELL, LOPEZ, ABDELHADY]], [6, 8, 2])
        perspectives = sources[CELL]['units']
        self.assertEqual([u['contributor'] for u in perspectives], [x[0] for x in m.CELL_THEMES])
        self.assertEqual(perspectives[0]['source_locator'], {'section_id': 'sec1.1', 'paragraph_id': 'p1'})
        self.assertIn(FILLER, perspectives[0]['original_paragraph'])
        self.assertEqual(sum('provisional' in u['evidence_confidence'] for u in perspectives), 4)
        self.assertEqual(sources[CELL]['xml_sha256'], e.sha((self.root / 'xml/W1.xml').read_bytes()))
        self.assertNotIn('Synthetic', json.dumps(summary))
        self.assertNotIn('original_paragraph', json.dumps(summary))
        for name in ['agenda-curated-units.json', 'agenda-curated-summary.json']:
            self.assertEqual((self.root / 'derived' / name).stat().st_mode & 0o077, 0)

    def test_box_groups_have_exact_xml_boundaries_and_external_pointers(self):
        m.curate(self.store)
        source = self.private()['sources'][LOPEZ]
        self.assertTrue(source['formal_agenda'])
        self.assertEqual([u['external_locator']['item_ordinal'] for u in source['units']], list(range(1, 9)))
        self.assertEqual([u['interrogatives'] for u in source['units']], [2, 3, 4, 2, 1, 3, 3, 1])
        for i, unit in enumerate(source['units']):
            self.assertEqual(unit['type'], 'formal_question_group')
            self.assertEqual(unit['source_locator']['textbox_id'], 'tb0005')
            self.assertEqual(unit['source_locator']['paragraph_id'], f'par{95 + i * 5:04d}')
            self.assertEqual(unit['xml_item_boundaries'], 'one_paragraph_per_group_verified')
            self.assertIn(FILLER, unit['original_paragraph'])

    def test_flattened_box_cannot_claim_eight_verified_boundaries(self):
        data = article(LOPEZ, '<textbox id="tb0005"><textbox-body><sections>'
                       f'<para id="flat">{FILLER}' + 'Synthetic question? ' * 19
                       + '</para></sections></textbox-body></textbox>')
        self.replace_source('W2', LOPEZ, data)
        with self.assertRaisesRegex(ValueError, 'unexpected_agenda_structure'):
            m.curate(self.store)
        self.assertFalse((self.root / 'derived').exists())

    def test_contextual_prompts_stay_two_blocks_not_six_agenda_items(self):
        m.curate(self.store)
        source = self.private()['sources'][ABDELHADY]
        self.assertFalse(source['formal_agenda'])
        self.assertEqual([u['interrogatives'] for u in source['units']], [3, 3])
        self.assertEqual([u['source_locator']['section_id'] for u in source['units']], ['sec1', 'sec4.5'])
        self.assertEqual({u['type'] for u in source['units']}, {'contextual_prompt_block'})

    def test_unexpected_structure_fails_before_output_or_overwrite(self):
        m.curate(self.store)
        previous = {p.name: p.read_bytes() for p in (self.root / 'derived').glob('agenda-curated-*.json')}
        for wid, doi, altered in [
                ('W1', CELL, cell().replace(b'sec1.6', b'sec1.7')),
                ('W2', LOPEZ, lopez().replace(b'Synthetic question? ', b'Synthetic statement. ', 1)),
                ('W3', ABDELHADY, abdelhady().replace(b'sec4.5', b'sec4.6'))]:
            with self.subTest(doi=doi):
                original = (self.root / f'xml/{wid}.xml').read_bytes()
                self.replace_source(wid, doi, altered)
                with self.assertRaisesRegex(ValueError, 'unexpected_agenda_structure'):
                    m.curate(self.store)
                self.assertEqual(previous, {p.name: p.read_bytes() for p in (self.root / 'derived').glob('agenda-curated-*.json')})
                self.replace_source(wid, doi, original)

    def test_corrupt_source_hash_and_dtd_fail_without_outputs(self):
        path = self.root / 'xml/W1.xml'
        path.write_bytes(path.read_bytes() + b' ')
        with self.assertRaisesRegex(ValueError, 'checksum'):
            m.curate(self.store)
        self.assertFalse((self.root / 'derived').exists())
        data = b'<!DOCTYPE x SYSTEM "file:///synthetic-secret">' + cell()
        path.write_bytes(data)
        row = e.latest(self.root / 'manifest.tsv')['W1']
        row['xml_sha256'] = e.sha(data)
        e.append(self.root / 'manifest.tsv', row, e.FIELDS)
        self.reviewed[CELL] = e.sha(data)
        with self.assertRaisesRegex(e.Rejected, 'dtd_or_entity'):
            m.curate(self.store)
        self.assertFalse((self.root / 'derived').exists())

    def test_unreviewed_revision_rejected_even_with_consistent_manifest(self):
        original_reviewed = self.reviewed[CELL]
        self.replace_source('W1', CELL, cell().replace(b'Synthetic heading', b'Revised synthetic heading'))
        self.reviewed[CELL] = original_reviewed
        with self.assertRaisesRegex(ValueError, 'unexpected_agenda_structure'):
            m.curate(self.store)
        self.assertFalse((self.root / 'derived').exists())

    def test_missing_source_and_duplicate_doi_fail_closed(self):
        manifest = self.root / 'manifest.tsv'
        original = manifest.read_bytes()
        rows = e.latest(manifest)
        manifest.write_text('\n'.join(original.decode().splitlines()[:-1]) + '\n')
        with self.assertRaisesRegex(ValueError, 'unexpected_agenda_structure'):
            m.curate(self.store)
        manifest.write_bytes(original)
        e.append(manifest, dict(rows['W1'], openalex_id='W4'), e.FIELDS)
        with self.assertRaisesRegex(ValueError, 'unexpected_agenda_structure'):
            m.curate(self.store)
        self.assertFalse((self.root / 'derived').exists())

    def test_default_mining_receipts_remain_unchanged_by_curation(self):
        expected = m.mine(self.store)
        names = ['agenda-question-candidates.tsv', 'agenda-summary.json']
        before = {name: (self.root / 'derived' / name).read_bytes() for name in names}
        self.assertEqual([expected['sources'][d]['candidate_count'] for d in [CELL, LOPEZ, ABDELHADY]], [15, 19, 6])
        m.curate(self.store)
        self.assertEqual(before, {name: (self.root / 'derived' / name).read_bytes() for name in names})
        self.assertEqual(m.mine(self.store), expected)

    def test_cli_returns_only_aggregate_enums_and_counts(self):
        for flag in [[], ['--curate']]:
            with self.subTest(flag=flag), patch('sys.argv', ['mine_elsevier.py', '--store', str(self.store), *flag]), \
                    contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(m.main(), 0)
            self.assertNotIn('Synthetic', out.getvalue())
            json.loads(out.getvalue())


if __name__ == '__main__':
    unittest.main()
