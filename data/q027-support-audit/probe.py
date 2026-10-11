# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas==2.3.3", "numpy==2.3.3"]
# ///
import importlib.util
from pathlib import Path
import numpy as np
import pandas as pd
root=Path(__file__).resolve().parents[2]
out=root/'scratch/q027-independent-audit'
out.mkdir(parents=True, exist_ok=True)
spec=importlib.util.spec_from_file_location('screen',root/'data/q027-joint-support/build.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
s.OUT=out;s.fetch=lambda:None
s.main()
for name in ['summary.tsv','per_stage.tsv']:
    print('identical',name,(out/name).read_bytes()==(root/'data/q027-joint-support'/name).read_bytes())
tab=pd.read_csv(out/'per_stage.tsv',sep='\t')
corrected=[]
for k in s.THRESHOLDS:
    col=f'three_bands_outside_ge{k}'
    row={'threshold_cells_per_band':k,'stages_total':len(tab),'stages_passing':int(tab[col].sum())}
    for era,older,younger in [('Palaeozoic',541,252.17),('Mesozoic',252.17,66),('Cenozoic',66,0)]:
        subset=tab[(tab.base_ma<=older+1e-6)&(tab.base_ma>younger+1e-6)]
        row[f'{era}_passing']=f'{int(subset[col].sum())}/{len(subset)}'
    corrected.append(row)
pd.DataFrame(corrected).to_csv(out/'corrected-era-summary.tsv',sep='\t',index=False)
print('Source-consistent era summary',corrected)
o=pd.read_csv(s.RAW/'occurrences.csv',usecols=s.COLUMNS,low_memory=False)
print('duplicate IDs',o.occurrence_no.duplicated().sum())
o=o[o.accepted_rank.isin(['genus','subgenus','species']) & o.genus.notna()]
o=o[o.lithification1.fillna('')!='unlithified']
o=o[o.paleolat.notna() & o.paleolng.notna()].copy()
print('pre stage n',len(o),'invalid age',((o.min_ma>o.max_ma)|o.min_ma.isna()|o.max_ma.isna()).sum(),'invalid coords',((o.paleolat.abs()>90)|(o.paleolng.abs()>180)).sum())
st=s.stages()
candidate=((o.min_ma.values[:,None]>=st.min_ma.values-1e-9)&(o.max_ma.values[:,None]<=st.max_ma.values+1e-9))
nc=candidate.sum(axis=1)
print('stage intervals',len(st),'candidate counts',pd.Series(nc).value_counts().sort_index().to_dict())
print('unused stages',st.interval_name[~candidate.any(axis=0)].to_list())
print('multi match sample',o.loc[nc>1,['occurrence_no','min_ma','max_ma']].head().to_dict('records'))
idx=np.clip(np.searchsorted(st.max_ma.values,o.max_ma.values-1e-9,side='left'),0,len(st)-1)
ok=(o.min_ma.values>=st.min_ma.values[idx]-1e-9)&(o.max_ma.values<=st.max_ma.values[idx]+1e-9)
o=o[ok].copy();o['stage']=st.interval_name.values[idx[ok]];o['eu_na']=o.cc.isin(s.europe_north_america_codes())
print('lost valid any candidate',int(((nc>0)&~ok).sum()),'multiple match retained',int((nc[ok]>1).sum()))
print('country n',o.cc.value_counts(dropna=False).to_dict())
codes=pd.read_csv(s.RAW/'country_codes.csv',keep_default_na=False)
print('unmapped country codes',o.loc[~o.cc.isin(set(codes['ISO3166-1-Alpha-2'])|{'UK'}),'cc'].value_counts(dropna=False).to_dict())
reg=pd.read_csv(s.RAW/'marine_regions.csv')
names={}
for col in ['official_name_en','CLDR display name']:
    for name,iso in zip(codes[col],codes['ISO3166-1-Alpha-2']):
        if name:names[name.strip().lower()]=iso
names.update({'united kingdom':'GB','moldova, republic of':'MD','bosnia & herzegovina':'BA','united states':'US'})
reg['iso']=reg.country_name.map(lambda n:names.get(n.strip().lower()))
reg.to_csv(out/'country-region-join.tsv',sep='\t',index=False)
print('all unmatched region names',reg.loc[reg.iso.isna(),'country_name'].to_list())
print('unmapped to region table',o.loc[~o.cc.replace({'UK':'GB'}).isin(reg.iso),'cc'].value_counts(dropna=False).to_dict())
o['abslat']=o.paleolat.abs();o['hemi']=np.where(o.paleolat>=0,'N','S')
def grid(deg,lat_offset=0,lon_offset=0):
    lat_i=np.floor((o.paleolat.values+90-lat_offset)/deg).astype(int)
    lat_mid=-90+lat_offset+(lat_i+.5)*deg
    nlon=np.maximum(1,np.round(360/deg*np.cos(np.radians(lat_mid)))).astype(int)
    lon_i=np.floor(((o.paleolng.values+180-lon_offset)%360)/360*nlon).astype(int)
    return lat_i*1000+lon_i
def counts(cell,eligible=None):
    p=o.assign(cell=cell)
    if eligible is not None:p=p[eligible]
    rows=[]
    for stage,g in p.groupby('stage'):
        row={'stage':stage}
        for a,b in [(0,20),(20,40),(40,90)]:
            q=g[(g.abslat>=a)&(g.abslat<b)]
            for label,r in [('outside',q[~q.eu_na]),('Noutside',q[(~q.eu_na)&(q.hemi=='N')]),('Soutside',q[(~q.eu_na)&(q.hemi=='S')])]:
                row[f'{label}_{a}_{b}']=r.cell.nunique()
        for label in ['outside','Noutside','Soutside']:
            for k in [3,10,20]:row[f'{label}_pass{k}']=all(row[f'{label}_{a}_{b}']>=k for a,b in [(0,20),(20,40),(40,90)])
        rows.append(row)
    return pd.DataFrame(rows)
configs=[('5deg',5,0,0),('5deg_shift',5,2.5,2.5),('9deg',9,0,0),('9deg_shift',9,4.5,4.5)]
for name,deg,la,lo in configs:
    c=counts(grid(deg,la,lo));c.to_csv(out/f'{name}-support.tsv',sep='\t',index=False)
    print(name,{col:int(c[col].sum()) for col in c if 'pass' in col})
c=grid(5);o['cell']=c
for threshold in [2,5,10]:
    outside=o[~o.eu_na]
    nums=outside.groupby(['stage','cell']).collection_no.nunique()
    eligible=np.array([nums.get((a,b),0)>=threshold for a,b in zip(o.stage,o.cell)])
    q=counts(c,eligible)
    print('min collections/cell',threshold,{col:int(q[col].sum()) for col in q if col.startswith('outside_pass')})
    q.to_csv(out/f'5deg-min{threshold}collections-support.tsv',sep='\t',index=False)
print('cells mixed region',int(o.groupby(['stage','cell']).eu_na.nunique().gt(1).sum()))
pool=o.groupby(['stage','cell']).agg(collections=('collection_no','nunique'),occurrences=('occurrence_no','size'),genera=('genus','nunique'),lat=('paleolat','mean'),eu_na_all=('eu_na','all'),eu_na_any=('eu_na','any')).reset_index()
pool.to_csv(out/'cell-diagnostics.tsv',sep='\t',index=False)
print('outside cells totals',len(pool[~pool.eu_na_all]),'with eu_na overlap',len(pool[(~pool.eu_na_all)&pool.eu_na_any]))
print('collections in multiple cells within stage',int(o.groupby(['stage','collection_no']).cell.nunique().gt(1).sum()))
print('collections in multiple stages',int(o.groupby('collection_no').stage.nunique().gt(1).sum()))
print('abs90 occurrences',int((o.abslat==90).sum()),'lon180',int((o.paleolng==180).sum()))
