"""Check retained G1/G2 replicate outputs against analytic moments."""
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys

root,output=map(Path,sys.argv[1:3]); out={'python_version':sys.version.split()[0], 'source_scope':'Retained G1/G2 tables only; no generator execution; G3/G3b/G5 not replayed','inputs':{},'generators':{}}
EN=math.exp((.3-.2)*15)
surv=(.3-.2)/(.3-.2*math.exp(-(.3-.2)*15))
for name in ['paleobuddy','treesim']:
    path=root/f'g1_{name}.tsv'
    out['inputs'][path.name]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}
    with path.open() as f: rows=list(csv.DictReader(f,delimiter='\t'))
    x=[int(r['extant']) for r in rows]; n=len(x); mean=statistics.mean(x); p=sum(v>0 for v in x)/n
    z=(mean-EN)/(statistics.stdev(x)/math.sqrt(n)); zs=(p-surv)/math.sqrt(surv*(1-surv)/n)
    usable=[r for r in rows if r['K']!='NA' and float(r['L'])>0]
    expected=[.5*float(r['L']) for r in usable]
    k=[int(r['K']) for r in usable]
    poisson_z=(sum(k)-math.fsum(expected))/math.sqrt(math.fsum(expected))
    disp=math.fsum((a-b)**2/b for a,b in zip(k,expected))/len(k)
    tol=3*math.sqrt(2/len(k))
    out['generators'][name]={'n':n,'mean_extant':mean,'truth_mean':EN,'z_mean':z,'survival':p,'truth_survival':surv,'z_survival':zs,
       'G1_pass':abs(z)<3 and abs(zs)<3,'G2_poisson_usable':len(k),'G2_poisson_z':poisson_z,'G2_dispersion':disp,'G2_tolerance':tol,'G2_pass':abs(poisson_z)<3 and abs(disp-1)<tol}
output.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['generators'],indent=2))
