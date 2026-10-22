-- NSB occurrences with synonymy resolved and the portal's default filters
-- (Renaudie et al. 2020, Fig. 3; NSBcompanion 2.1 getNeptuneData), plus the
-- portal's exclusion of undated samples. Runs on the SQLite snapshots.
-- Ages are GTS2012 point estimates from each hole's current age model.
with recursive resolve(taxon_id, current_id, depth) as (
    select taxon_id, taxon_id, 0 from neptune_taxonomy
    union all
    select r.taxon_id, t.taxon_synon_to, r.depth + 1
    from resolve r join neptune_taxonomy t on t.taxon_id = r.current_id
    where t.taxon_synon_to is not null and t.taxon_synon_to <> t.taxon_id and r.depth < 20
),
terminal as (
    select taxon_id, current_id as resolved_id
    from resolve r
    where depth = (select max(depth) from resolve r2 where r2.taxon_id = r.taxon_id)
)
select
    st.sample_id,
    s.fossil_group,
    st.taxon_id                       as original_taxon_id,
    t.taxon_name                      as original_name,
    t.taxon_status                    as original_status,
    rt.taxon_id                       as resolved_taxon_id,
    rt.genus                          as resolved_genus,
    rt.species                        as resolved_species,
    rt.subspecies                     as resolved_subspecies,
    rt.taxon_status                   as resolved_status,
    st.taxon_abundance,
    s.sample_group_abundance,
    s.sample_preservation,
    s.hole_id,
    hs.latitude,
    hs.longitude,
    hs.ocean_code,
    s.sample_depth_mbsf,
    s.sample_age_ma,
    s.paleo_latitude,
    s.paleo_longitude,
    amh.age_quality,
    s.dataset_id,
    so.source_citation
from neptune_sample_taxa st
join neptune_sample s on s.sample_id = st.sample_id
join neptune_taxonomy t on t.taxon_id = st.taxon_id
join terminal tm on tm.taxon_id = st.taxon_id
join neptune_taxonomy rt on rt.taxon_id = tm.resolved_id
join neptune_hole_summary hs on hs.hole_id = s.hole_id
left join neptune_age_model_history amh on amh.site_hole = hs.site_hole and amh.current_flag = 'Y'
left join neptune_sod_off so on so.dataset_id = s.dataset_id
where t.taxon_status in ('V', 'S', 'B')
  and (st.taxon_qualifier is null or st.taxon_qualifier = '')
  and (s.sample_status is null or s.sample_status not in ('c', 'w'))
  and s.sample_age_ma is not null;
