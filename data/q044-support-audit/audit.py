# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas==2.3.3", "numpy==2.3.3"]
# ///
"""Bounded Q044 audit; import existing screen, redirect all outputs into this folder.
Run: uv run data/q044-support-audit/audit.py from repository root.
Raw input is ignored local Close2019 archive, identified in screen README.
No richness estimator is fitted. Output describes observed recorded identities only.
"""
from pathlib import Path
import importlib.util, json, argparse
from collections import Counter
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--out', type=Path, default=ROOT / 'scratch/q044-independent-audit')
args = parser.parse_args()
OUT = args.out.resolve()
OUT.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('screen', ROOT / 'data/q044-joint-support/build.py')
screen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(screen)
screen.OUT = OUT / 'baseline'
screen.OUT.mkdir(exist_ok=True)
screen.main()
# Require byte-identical baseline reproduction of every tracked result.
for name in ('per_bin.tsv', 'per_window.tsv', 'summary.tsv'):
    assert (screen.OUT / name).read_bytes() == (ROOT / 'data/q044-joint-support' / name).read_bytes(), name
occ, n0 = screen.clean()
bins = pd.read_csv(screen.SRC / 'input-data/equal-length-intervals.csv')
k = np.searchsorted(bins.FAD.values, occ.ma_mid.values, side='right')
k = np.clip(k, 0, len(bins)-1)
inside = ((occ.ma_mid.values < bins.FAD.values[k]) & (occ.ma_mid.values >= bins.LAD.values[k])
          & ~np.isin(occ.ma_mid.values, bins.FAD.values))
occ = occ[inside].copy()
occ['bin'] = bins.bin.values[k[inside]]
raw = pd.read_csv(screen.DL / 'alpha_tetrapodomorpha.csv', usecols=['occurrence_no','accepted_no','accepted_name'], keep_default_na=False)
occ = occ.merge(raw[['occurrence_no', 'accepted_no','accepted_name']].rename(columns={'accepted_name':'raw_accepted_name'}), on='occurrence_no',validate='one_to_one')
rows, wrows, taxa_rows = [], [], []
for b in screen.FOCUS:
    g = occ[occ.bin == b]
    colls = g.groupby('collection_no').agg(paleolat=('paleolat','first'),paleolng=('paleolng','first')).reset_index()
    sets, ids_sets, gen_sets, ns, alphas = [], [], [], [], []
    for j, (centre,members) in enumerate(screen.windows(colls,1000,10),1):
        wc = colls.iloc[members]
        wo = g[g.collection_no.isin(wc.collection_no)]
        sp = wo[wo.binomial != '']
        ss = set(sp.binomial)
        sets.append(ss); ids_sets.append(set(sp.accepted_no)); gen_sets.append(set(wo.loc[wo.genus_name!='','genus_name']))
        ns.append(len(wc))
        ar = sp.groupby('collection_no').binomial.nunique().reindex(wc.collection_no,fill_value=0)
        alphas.append(ar.mean())
        wrows.append(dict(bin=b,window=j,collections=len(wc),species_collections=int((ar>0).sum()),empty_species_collections=int((ar==0).sum()),species=len(ss),alpha_all_collections=ar.mean(),alpha_species_collections=ar[ar>0].mean(),species_occurrences=len(sp),range_crosses_bin=int(((wo.max_ma>bins.set_index('bin').loc[b,'FAD']) | (wo.min_ma<bins.set_index('bin').loc[b,'LAD'])).sum()),occurrences=len(wo)))
    for label,ss in [('species_name',sets),('accepted_no',ids_sets),('genus_name',gen_sets)]:
        mult=Counter(x for s in ss for x in s)
        K=len(ss); gamma=len(mult); memberships=sum(mult.values()); shared=sum(v>=2 for v in mult.values())
        f=shared/gamma if gamma else np.nan; mm=memberships/gamma if gamma else np.nan
        beta=K*gamma/memberships if memberships else np.nan
        gw=np.array([len(s) for s in ss]); ps=np.array(ns)/sum(ns)
        beta_coll=gamma/np.dot(ps,gw) if np.dot(ps,gw)>0 else np.nan
        rows.append(dict(bin=b,level=label,K=K,empty_species_windows=sum(len(s)==0 for s in ss),union_taxa=gamma,sum_window_taxa=memberships,shared_taxa=shared,f_shared=f,shared_mean_multiplicity=np.mean([v for v in mult.values() if v>=2]) if shared else np.nan,mean_multiplicity=mm,beta_equal=beta,beta_over_K=beta/K,lower_bound=1/(1+(K-1)*f),upper_bound=1/(1+f),max_increase_factor_to_equal_weight_ceiling=mm,beta_collection_weighted=beta_coll,beta_collection_weighted_over_K=beta_coll/K))
        taxa_rows.extend(dict(bin=b,level=label,taxon=x,multiplicity=v) for x,v in mult.items() if v>=2)
    if sets:
        Gamma=len(set().union(*sets)); gbar=np.mean([len(s) for s in sets]); abar=np.mean(alphas)
        assert np.isclose(Gamma,abar*(gbar/abar)*(Gamma/gbar))
# Taxonomic/geometry/time sanity checks; no corrections silently applied.
# Pure mathematical counterexample: every taxon biologically occupies K windows,
# independent per-window detection d, conditional on being recorded at least once.
counterexamples=[]
for K in (4,8):
    for d in (.01,.02,.1):
        mean_recorded_multiplicity=K*d/(1-(1-d)**K)
        counterexamples.append(dict(K=K,detection_probability=d,latent_beta=1,conditional_expected_recorded_multiplicity=mean_recorded_multiplicity,large_pool_observed_beta=K/mean_recorded_multiplicity,large_pool_observed_beta_over_K=1/mean_recorded_multiplicity))
pd.DataFrame(counterexamples).to_csv(OUT/'detection_counterexample.tsv',sep='\t',index=False)
sp=occ[occ.binomial!='']
name_collisions=sp.groupby('binomial').accepted_no.nunique()
id_names=sp.groupby('accepted_no').binomial.nunique()
collection_fields=occ.groupby('collection_no')[['paleolat','paleolng','max_ma','min_ma']].nunique()
checks=dict(download_occurrences=n0,clean_binned_occurrences=len(occ),baseline_byte_identical=True,species_occurrences=len(sp),binomial_distinct_accepted_ids_gt1=int((name_collisions>1).sum()),accepted_id_distinct_binomials_gt1=int((id_names>1).sum()),subspecies_occurrences=int((sp.accepted_rank=='subspecies').sum()),nonpositive_or_reversed_ranges=int((occ.max_ma<occ.min_ma).sum()),coordinates_out_of_domain=int(((occ.paleolat.abs()>90)|(occ.paleolng.abs()>180)).sum()),collections_inconsistent_fields={x:int((collection_fields[x]>1).sum()) for x in collection_fields},raw_name_parenthesis_occurrences=int(sp.raw_accepted_name.str.contains(r'\(',regex=True).sum()))
df = pd.DataFrame(rows)
df.to_csv(OUT/'multiplicity_beta.tsv',sep='\t',index=False)
compact_cols = ['bin','K','empty_species_windows','union_taxa','sum_window_taxa','shared_taxa','shared_mean_multiplicity','beta_equal','beta_over_K','max_increase_factor_to_equal_weight_ceiling']
df.loc[df.level == 'species_name',compact_cols].to_csv(OUT/'compact_species_beta.tsv',sep='\t',index=False)
pd.DataFrame(wrows).to_csv(OUT/'window_identity_support.tsv',sep='\t',index=False)
pd.DataFrame(taxa_rows).to_csv(OUT/'shared_taxa.tsv',sep='\t',index=False)
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
print(pd.DataFrame(rows).query("level == 'species_name'").to_string(index=False))
