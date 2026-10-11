# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas==2.3.3", "numpy==2.3.3"]
# ///
"""Compare age rules and basic richness eligibility; not the Benson pipeline."""
import hashlib
import importlib.util
from pathlib import Path
import numpy as np
import pandas as pd
root=Path(__file__).resolve().parents[2];out=root/'scratch/q027-independent-audit'
out.mkdir(parents=True, exist_ok=True)
spec=importlib.util.spec_from_file_location('screen',root/'data/q027-joint-support/build.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
o=pd.read_csv(s.RAW/'occurrences.csv',usecols=s.COLUMNS,low_memory=False,keep_default_na=False,na_values={c:[''] for c in s.COLUMNS if c!='cc'})
o=o[o.accepted_rank.isin(['genus','subgenus','species']) & o.genus.notna()]
o=o[o.lithification1.fillna('')!='unlithified']
o=o[o.paleolat.notna() & o.paleolng.notna()].copy()
st=s.stages();duration=o.max_ma.values-o.min_ma.values
overlap=np.maximum(0,np.minimum(o.max_ma.values[:,None],st.max_ma.values)-np.maximum(o.min_ma.values[:,None],st.min_ma.values))
majority=overlap>duration[:,None]/2
counts=majority.sum(axis=1)
print('majority candidate counts',pd.Series(counts).value_counts().sort_index().to_dict(),flush=True)
idx=majority.argmax(axis=1)
contain=((o.min_ma.values>=st.min_ma.values[idx]-1e-9)&(o.max_ma.values<=st.max_ma.values[idx]+1e-9))
print('added by majority',int(((counts==1)&~contain).sum()),'zero duration',int((duration==0).sum()),flush=True)
o=o[counts==1].copy();o['stage']=st.interval_name.values[idx[counts==1]]
o['contained']=contain[counts==1];o['eu_na']=o.cc.isin(s.europe_north_america_codes());o['abslat']=o.paleolat.abs()
lat_i=np.floor((o.paleolat.values+90)/5).astype(int);mid=-90+(lat_i+.5)*5
nlon=np.maximum(1,np.round(72*np.cos(np.radians(mid)))).astype(int)
o['cell']=lat_i*1000+np.floor((o.paleolng.values+180)/360*nlon).astype(int)
print('retained cc missing/literalNA',o.loc[o.contained,'cc'].value_counts().reindex(['','NA'],fill_value=0).to_dict(),flush=True)
def summary(p,label):
    rows=[]
    for stage,g in p.groupby('stage'):
        r={'stage':stage,'rule':label,'occurrences':len(g)}
        for a,b in [(0,20),(20,40),(40,90)]:r[f'outside_{a}_{b}']=g[(~g.eu_na)&(g.abslat>=a)&(g.abslat<b)].cell.nunique()
        for k in [3,10,20]:r[f'pass{k}']=all(r[f'outside_{a}_{b}']>=k for a,b in [(0,20),(20,40),(40,90)])
        rows.append(r)
    t=pd.DataFrame(rows);t.to_csv(out/f'{label}-support.tsv',sep='\t',index=False)
    print(label,'occurrences',len(p),'stages',len(t),{f'k{k}':int(t[f'pass{k}'].sum()) for k in [3,10,20]},flush=True)
    return t
base=summary(o[o.contained],'contained-check')
major=summary(o,'majority')
change=base.merge(major,on='stage',suffixes=('_contained','_majority'))
print('new k10 majority stages',change.loc[(~change.pass10_contained)&change.pass10_majority,'stage'].to_list(),flush=True)
print('lost k10 majority stages',change.loc[change.pass10_contained&(~change.pass10_majority),'stage'].to_list(),flush=True)
valid=set(pd.read_csv(s.RAW/'country_codes.csv',keep_default_na=False)['ISO3166-1-Alpha-2'])|{'UK','AA'}
valid.discard('')
summary(o[o.contained & o.cc.isin(valid)],'known-country')
dedup=o[o.contained & ~o.eu_na].drop_duplicates(['stage','cell','collection_no','genus'])
freq=dedup.groupby(['stage','cell','genus']).collection_no.nunique().reset_index(name='incidence')
elig=freq.groupby(['stage','cell']).agg(genera=('genus','size'),max_incidence=('incidence','max'))
keys=set(elig[(elig.genera>=3)&(elig.max_incidence>1)].index)
p=o[o.contained].copy();mask=np.array([(a,b) in keys for a,b in zip(p.stage,p.cell)])
summary(p[mask],'basic-incidence-eligible')
print('eligible outside cells',len(keys),'outside cells',len(elig),flush=True)
for stage in ['Changhsingian','Induan','Aptian','Albian','Cenomanian','Turonian','Coniacian','Santonian','Ypresian','Lutetian','Burdigalian']:
    print('stage',stage,change[change.stage==stage][['outside_0_20_contained','outside_20_40_contained','outside_40_90_contained','outside_0_20_majority','outside_20_40_majority','outside_40_90_majority']].to_dict('records'),flush=True)
sha=[]
for f in sorted((out/'source').rglob('*')):
    if f.is_file():sha.append({'member':str(f.relative_to(out/'source')),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
pd.DataFrame(sha).to_csv(out/'source-member-checksums.tsv',sep='\t',index=False)
