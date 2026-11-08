"""Read retained case outputs; recalculate coverage and analytic SS bound."""
import csv
import hashlib
import json
import math
from pathlib import Path
import sys

root, output = map(Path, sys.argv[1:3])
z=1.959963984540054
def score(rows,column):
    assert all(r[column]!='NA' for r in rows)
    n=len(rows); k=sum(float(r['te_fwd']) <= float(r[column]) for r in rows)
    q=k/n; d=1+z*z/n; c=(q+z*z/(2*n))/d
    h=z*math.sqrt(q*(1-q)/n+z*z/(4*n*n))/d
    return {'covered':k,'n':n,'coverage':q,'wilson95_casewise_descriptive':[c-h,c+h],'casewise_binomial_mc_se':math.sqrt(q*(1-q)/n)}
res={'method':'Python CSV and scalar arithmetic; analytic continuous Strauss-Sadler one-sided bound from n, range, last',
     'python_version':sys.version.split()[0],'inputs':{},'arms':{}}
allrows={}
for arm in 'ABC':
    p=root/f't2_extinction_{arm}.tsv'
    res['inputs'][p.name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
    with p.open() as f: raw=list(csv.DictReader(f,delimiter='\t'))
    rows=[r for r in raw if r['dropped']=='0']; allrows[arm]=rows
    methods={c:score(rows,c) for c in ['tbea_ss_upper','ede_ss_upper','ede_robson_upper']}
    discrepancies=[abs(float(r['tbea_ss_upper'])-(float(r['last'])+float(r['range'])*math.expm1(-math.log(.05)/(int(r['n'])-1)))) for r in rows]
    agreement=sum(abs(float(r['tbea_ss_upper'])-float(r['ede_ss_upper']))<=.02 for r in rows)
    discrete=sum(abs(float(r['tbea_ss_upper_disc'])-float(r['ede_ss_upper']))<=1e-6 for r in rows)
    out={'original_cases':len(raw),'retained':len(rows),'dropped':len(raw)-len(rows),'methods':methods,
         'continuous_ss_analytic_max_abs_difference':max(discrepancies),'ss_agreement_within_0_02':agreement/len(rows),
         'discretised_ss_agreement_within_1e_6':discrete/len(rows)}
    if arm=='B':
        out['by_extinction_class']={c:{'n':sum(r['te_class']==c for r in rows), 'tbea_ss':score([r for r in rows if r['te_class']==c],'tbea_ss_upper')} for c in sorted(set(r['te_class'] for r in rows))}
    res['arms'][arm]=out
A=res['arms']['A']
n=A['retained']
probabilities=[math.exp(math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)+k*math.log(.95)+(n-k)*math.log(.05)) for k in range(n+1)]
def binomial_quantile(p):
    cumulative=0
    for k,probability in enumerate(probabilities):
        cumulative+=probability
        if cumulative>=p: return k/n
band=[binomial_quantile(.005),binomial_quantile(.995)]
res['E4']={'nominal_99pct_binomial_acceptance_band':band,
    'both_ss_coverages_in_band':all(band[0]<=A['methods'][c]['coverage']<=band[1] for c in ['tbea_ss_upper','ede_ss_upper']),
    'ss_agreement_99pct':A['ss_agreement_within_0_02']>=.99}
res['E4']['overall_pass']=all(res['E4'][k] for k in ['both_ss_coverages_in_band','ss_agreement_99pct'])
a={r['case']:r for r in allrows['A']}; paired=[a[r['case']] for r in allrows['B']]
res['paired_arm_A_for_retained_B']={'tbea_ss':score(paired,'tbea_ss_upper'),'mean_fossils_A':sum(int(r['n']) for r in paired)/len(paired),'mean_fossils_B':sum(int(r['n']) for r in allrows['B'])/len(paired)}
output.write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'A':A,'B':res['arms']['B']['methods'],'E4':res['E4']},indent=2))
