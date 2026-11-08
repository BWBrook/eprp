"""Score saved proposal vectors without importing the model or replay scorer."""
import hashlib
import io
import json
import math
from pathlib import Path
import sys
import zipfile
import numpy as np

archive=Path(sys.argv[1]); out=Path(sys.argv[2])
z=zipfile.ZipFile(archive)
names=['INDITEK_2.0/data/observed_D.npz','INDITEK_2.0/output_data/inditekMCMCoutput_5002_proof.npz']
content={n:z.read(n) for n in names}
observation=np.load(io.BytesIO(content[names[0]]),allow_pickle=False)['proof']
chain=np.load(io.BytesIO(content[names[1]]),allow_pickle=False)
observed=observation[np.isfinite(observation)].tolist()
rows=[]
for c,t in [(0,50),(0,500),(5,5000)]:
    pred=chain['D'][t//50,:,c].tolist()
    assert len(pred)==len(observed)==2978 and all(map(math.isfinite,pred))
    score=math.fsum((p-y)*(p-y)/4 for p,y in zip(pred,observed))
    saved=float(chain['rss_proposed_history'][t,c])
    rows.append({'chain_zero_based':c,'iteration':t,'saved_prediction_index':t//50,
      'acceptance_flag':int(chain['acceptance_history'][t,c]),
      'parameters':chain['params_proposed_history'][t,:,c].tolist(),
      'finite_cells':len(pred),'saved_rss':saved,'saved_vector_rescored_with_fsum':score,
      'saved_score_minus_independent_rescore':saved-score,
      'parameters_differ_from_next_accepted_state':bool(np.any(chain['params_proposed_history'][t,:,c]!=chain['params_accepted_history'][t+1,:,c]))})
result={'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
        'member_sha256':{k:hashlib.sha256(v).hexdigest() for k,v in content.items()},
        'versions':{'python':sys.version.split()[0],'numpy':np.__version__},
        'method':'Read NPZ members directly from pinned ZIP; fsum of squared residuals divided by 4 on deposited finite observed cells; no model import',
        'results':rows}
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(rows,indent=2))
