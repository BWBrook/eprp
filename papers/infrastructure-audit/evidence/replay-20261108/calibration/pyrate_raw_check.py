"""Reaggregate retained logs; no PyRate fit or original summarizer is called."""
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys
import numpy as np

root, destination = map(Path, sys.argv[1:3])
manifest = []
def track(path):
    manifest.append({'path': str(path.relative_to(root)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size})
    return path

def quantile(values, p):
    values = sorted(values)
    index = (len(values)-1)*p
    i = int(index)
    return values[i] + (values[min(i+1,len(values)-1)]-values[i])*(index-i)

def effective_size(values):
    x = np.array(values)-statistics.mean(values)
    # Direct lag products are independent of the original FFT implementation.
    products = np.correlate(x, x, mode='full')[len(x)-1:]
    rho = products/products[0]
    pairs = rho[:len(rho)//2*2].reshape(-1,2).sum(axis=1)
    stop = next((i for i,v in enumerate(pairs) if v < 0), len(pairs))
    return len(x)/(2*sum(pairs[:stop])-1)

def wilson(k,n):
    z=1.959963984540054
    d=1+z*z/n
    c=(k/n+z*z/(2*n))/d
    h=z*math.sqrt(k/n*(1-k/n)/n+z*z/(4*n*n))/d
    return [c-h,c+h]

with track(root/'e2_pyrate_reps.tsv').open() as f:
    stored = {r['rep']:r for r in csv.DictReader(f,delimiter='\t')}
results=[]
rounding_failures=[]
coverage_mismatches=[]
max_ess_relative_error=0
for arm in ['high','low']:
    truth=json.loads(track(root/f'truth_{arm}.json').read_text())
    for name,t in sorted(truth['reps'].items()):
        files=list((root/'runs'/name/'pyrate_mcmc_logs').glob('*_mcmc.log'))
        assert len(files)==1, (name,files)
        with track(files[0]).open() as f:
            raw=list(csv.DictReader(f,delimiter='\t'))
        assert [int(r['it']) for r in raw]==list(range(0,2000001,2000))
        stdout=track(root/'runs'/name/'stdout.txt').read_text()
        assert 'PyRate - v3.1.3 - 20260823' in stdout and 'Module FastPyRateC was loaded.' in stdout
        raw=raw[len(raw)//5:]
        assert len(raw)==int(stored[name]['n_samples'])==801
        track(root/'inputs'/f'{name}.py')
        row={'arm':arm,'rep':name,'retained_draws':len(raw),'parameters':{}}
        for p,col in [('lambda','lambda_0'),('mu','mu_0'),('q','q_rate')]:
            x=[float(r[col]) for r in raw]
            lo,med,hi=[quantile(x,z) for z in [.025,.5,.975]]
            ess=effective_size(x)
            covered=lo <= t[p] <= hi
            row['parameters'][p]={'truth':t[p],'lo':lo,'median':med,'hi':hi,'ess':ess,'covered':covered,'posterior_sd':statistics.stdev(x)}
            for label,value in [('lo',lo),('med',med),('hi',hi),('ess',ess)]:
                if format(value,'.6g') != format(float(stored[name][f'{p}_{label}']),'.6g'):
                    rounding_failures.append([name,p,label])
            max_ess_relative_error=max(max_ess_relative_error,abs(ess/float(stored[name][f'{p}_ess'])-1))
            if covered!=bool(int(stored[name][f'{p}_cov'])): coverage_mismatches.append([name,p])
        results.append(row)
summary={}
for arm in ['high','low']:
    rows=[r for r in results if r['arm']==arm]
    summary[arm]={'replicates':len(rows),'parameters':{}}
    for p in ['lambda','mu','q']:
        values=[r['parameters'][p] for r in rows]
        n=len(values); k=sum(v['covered'] for v in values)
        summary[arm]['parameters'][p]={'covered':k,'n':n,'coverage':k/n,'wilson95':wilson(k,n),
            'binomial_mc_se_at_observed_coverage':math.sqrt(k/n*(1-k/n)/n),
            'median_relative_bias':statistics.median(v['median']/v['truth']-1 for v in values),
            'misses_truth_below_lower':sum(v['truth']<v['lo'] for v in values),
            'misses_truth_above_upper':sum(v['truth']>v['hi'] for v in values),
            'minimum_ess':min(v['ess'] for v in values),
            'mean_posterior_sd_over_truth':statistics.mean(v['posterior_sd']/v['truth'] for v in values),
            'median_posterior_sd_over_truth':statistics.median(v['posterior_sd']/v['truth'] for v in values),
            'across_replicate_sd_of_medians_over_truth':statistics.stdev(v['median']/v['truth'] for v in values),
            'median_standardized_bias':statistics.median((v['median']-v['truth'])/v['posterior_sd'] for v in values)}
summary['high']['declared_E2_pass']=all(summary['high']['parameters'][p]['covered']>=90 for p in ['lambda','mu','q'])
summary['low']['declared_pass_criterion']=None
receipt={'method':'raw log CSV parsing, sorted linear-interpolation quantiles, direct lag-product initial-positive-pair ESS',
 'versions':{'python':sys.version.split()[0],'numpy':np.__version__},'summary':summary,
 'comparison_to_six_significant_digit_original_tsv':{'rounding_mismatches':rounding_failures,'coverage_mismatches':coverage_mismatches,'max_ess_relative_error':max_ess_relative_error},
 'inputs':manifest}
destination.write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
(destination.parent/'pyrate_raw_per_replicate.json').write_text(json.dumps(results,indent=2,allow_nan=False)+'\n')
print(json.dumps({'summary':summary,'rounding_mismatches':rounding_failures,'coverage_mismatches':coverage_mismatches},indent=2))
