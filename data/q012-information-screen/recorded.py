# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["numpy==2.1.3", "scipy==1.15.3"]
# ///
"""Prospectively fixed recorded-only mortality-proxy detector."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import time

import numpy as np
from scipy.stats import binom

import screen as O

HERE = Path(__file__).resolve().parent
P = json.loads((HERE/"recorded-protocol.json").read_text())
H0 = np.asarray(O.GEN.CFG["generator"]["h0_by_3Myr_bin_Ma"],float)
NODES, WEIGHTS = np.polynomial.hermite.hermgauss(P["quadrature_nodes"])


def cumulative_hazard(origin_ma, end_ma, baseline=H0):
    if not (0 <= end_ma <= origin_ma <= 75):
        raise ValueError("Recorded age outside ordered 0-75 Ma range")
    lower = 3*np.arange(len(baseline))
    return float(np.dot(baseline,np.maximum(0,np.minimum(origin_ma,lower+3)-np.maximum(end_ma,lower))))


def risk_proxy(hazard, extinction, nodes=NODES, weights=WEIGHTS):
    hazard, extinction = np.asarray(hazard,float), np.asarray(extinction,float)
    if np.any(hazard < 0) or np.any((extinction != 0) & (extinction != 1)):
        raise ValueError("Invalid hazard or extinction indicator")
    sigma=P["sigma"]
    x=sigma*math.sqrt(2)*nodes
    logweight=np.log(weights)[None,:]+extinction[:,None]*x-hazard[:,None]*np.exp(x-.5*sigma**2)
    shifted=np.exp(logweight-np.max(logweight,axis=1,keepdims=True))
    return np.sum(shifted*(x/sigma),axis=1)/np.sum(shifted,axis=1)


def features(observed):
    ids=observed["ids"]
    n=len(ids)
    if not n:
        return np.zeros(len(P["features"]))
    hazard=np.array([cumulative_hazard(observed["tO"][i],observed["tE"][i]) for i in ids])
    delta=np.array([observed["label"][i]=="ext" for i in ids],float)
    q=risk_proxy(hazard,delta)
    pos={i:k for k,i in enumerate(ids)}
    mean=float(q.mean())
    edge_sum,centered_sum,edges=0.0,0.0,0
    children={}
    for child in ids:
        parent=observed["par"][child]
        if parent < 0:
            continue
        qp,qd=q[pos[parent]],q[pos[child]]
        edge_sum+=qp*qd
        centered_sum+=(qp-mean)*(qd-mean)
        edges+=1
        children.setdefault(parent,[]).append(qd)
    sister_sum,sisters=0.0,0
    for daughters in children.values():
        a=np.asarray(daughters)
        sister_sum+=float((a.sum()**2-a@a)/2)
        sisters+=len(a)*(len(a)-1)//2
    return np.array([edge_sum/math.sqrt(1+edges),centered_sum/math.sqrt(1+edges),
                     sister_sum/math.sqrt(1+sisters),math.log1p(n),
                     sum(observed["label"][i]=="present" for i in ids)/n,float(delta.mean()),
                     mean,float(np.mean(q*q))])


def fit_discriminant(development_null,development_alternative):
    a,b=np.asarray(development_null,float),np.asarray(development_alternative,float)
    if a.ndim!=2 or b.ndim!=2 or a.shape[1]!=len(P["features"]) or b.shape[1]!=a.shape[1]:
        raise ValueError("Development features have wrong shape")
    both=np.vstack([a,b])
    location=both.mean(axis=0)
    scale=both.std(axis=0)
    scale[scale==0]=1
    a,b=(a-location)/scale,(b-location)/scale
    ma,mb=a.mean(axis=0),b.mean(axis=0)
    covariance=((a-ma).T@(a-ma)+(b-mb).T@(b-mb))/(len(a)+len(b)-2)
    reg=P["covariance_regularization"]
    covariance=reg["empirical_weight"]*covariance+reg["identity_weight"]*np.eye(len(ma))
    weights=np.linalg.solve(covariance,mb-ma)
    return dict(location=location.tolist(),scale=scale.tolist(),weights=weights.tolist(),
                standardized_null_mean=ma.tolist(),standardized_alternative_mean=mb.tolist())


def score(features_array,coefficients):
    return float(((np.asarray(features_array)-coefficients["location"])/coefficients["scale"])@coefficients["weights"])


def choose_threshold(calibration_scores):
    if set(calibration_scores)!={"calibration_null","calibration_zero"}:
        raise ValueError("Threshold may use only both endpoint-null calibration panels")
    failure=P["simultaneous_error_budget"]["per_null_upper_quantile_failure"]
    details={}
    for name,values in calibration_scores.items():
        n=len(values)
        rank=int(binom.ppf(1-failure,n,1-P["alpha"]))+1
        if rank>n:
            raise ValueError("Calibration panel too small for a finite upper threshold")
        details[name]=dict(upper_threshold=float(np.sort(values)[rank-1]),rank=rank,n=n,
                           exact_upper_quantile_coverage=float(binom.cdf(rank-1,n,1-P["alpha"])))
    return dict(threshold=max(v["upper_threshold"] for v in details.values()),calibration=details)


def evaluate_scores(evaluation_scores,threshold):
    if set(evaluation_scores)!={"evaluation_null","evaluation_zero","evaluation_alternative"}:
        raise ValueError("Expected three independent evaluation panels")
    result={}
    for name,values in evaluation_scores.items():
        n=len(values)
        k=int(np.sum(np.asarray(values)>threshold))
        result[name]=dict(successes=k,n=n,estimate=k/n,descriptive_cp95=O.cp_interval(k,n))
    alt=result["evaluation_alternative"]
    tail=P["simultaneous_error_budget"]["per_ensemble_power_lower_failure"]
    lower,upper=O.cp_interval(alt["successes"],alt["n"],tail)
    alt["simultaneous_power_interval"]=[lower,upper]
    nulls=[result[k] for k in ("evaluation_null","evaluation_zero")]
    passed=(alt["estimate"]>=.8 and lower>=.75 and all(r["estimate"]<=.05 and r["descriptive_cp95"][1]<=.07 for r in nulls))
    result["contract_inspired_detector_targets_pass"]=passed
    result["stronger_power_lower_bound_gt_08"]=lower>.8
    result["interpretation"]=("This fixed recorded detector meets the declared detector-only targets for the two endpoint nulls."
                              if passed else "This fixed recorded detector does not meet all declared detector-only targets; this is not an impossibility result.")
    return result


def replicate(seed,eta,ensemble):
    lineages,info=O.GEN.generate(seed,{"rho":eta/P["sigma"],"sigma":P["sigma"],"lambda0":ensemble["lambda0"]})
    observed,oi=O.GEN.observe(lineages,seed+1000000000)
    return dict(seed=seed,eta=eta,features=features(observed).tolist(),
                true_lineages=len(lineages),capped=info["capped"],recorded=oi["recorded"],
                recorded_labels=oi["labels"])


def describe(rows):
    total=sum(r["recorded"] for r in rows)
    return dict(n=len(rows),capped=sum(r["capped"] for r in rows),
                recorded_quantiles=dict(zip(("q05","median","q95"),np.quantile([r["recorded"] for r in rows],[.05,.5,.95]).tolist())),
                pooled_present_share=sum(r["recorded_labels"]["present"] for r in rows)/total if total else None)


def source_hashes():
    paths=[HERE/"recorded.py",HERE/"recorded-protocol.json",HERE/"recorded-design.md"]
    return dict(**O.hashes(),**{str(p.relative_to(HERE.parent.parent)):sha256(p) for p in paths})


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def panel(ensemble,name,handle,coefficients=None,smoke=False):
    settings=P["panels"][name]
    n=P["smoke"]["n_per_ensemble_per_hypothesis"] if smoke else settings["n"]
    ei=P["ensembles"].index(ensemble)
    pi=list(P["panels"]).index(name)
    start=P["smoke"]["seed_start"]+ei*100+pi*10 if smoke else ensemble["seed_base"]+settings["seed_offset"]
    rows=[]
    for seed in range(start,start+n):
        row=dict(ensemble=ensemble["name"],panel=name,**replicate(seed,settings["eta"],ensemble))
        if coefficients is not None:
            row["score"]=score(row["features"],coefficients)
        handle.write(json.dumps(row,allow_nan=False)+"\n")
        rows.append(row)
    handle.flush()
    print(json.dumps(dict(ensemble=ensemble["name"],panel=name,n=n)),flush=True)
    return rows


def run(mode,output,coefficient_path=None,expected_sha256=None):
    output.mkdir(parents=True,exist_ok=True)
    if (output/"rows.jsonl").exists() or (output/"summary.json").exists():
        raise FileExistsError("Preserve existing output: choose a new directory")
    frozen=None
    if mode=="evaluate":
        if coefficient_path is None or expected_sha256 is None:
            raise ValueError("Evaluation requires frozen coefficient path and explicit expected SHA256")
        if sha256(coefficient_path)!=expected_sha256:
            raise ValueError("Frozen coefficient SHA256 mismatch")
        frozen=json.loads(coefficient_path.read_text())
        if frozen["source_sha256"]!=source_hashes():
            raise ValueError("Evaluation source differs from development source freeze")
    t0=time.monotonic()
    results={}
    coefficients={}
    with (output/"rows.jsonl").open("x") as handle:
        for ensemble in P["ensembles"]:
            name=ensemble["name"]
            if mode in ("smoke","develop"):
                panels={k:panel(ensemble,k,handle,smoke=mode=="smoke") for k in ("development_null","development_alternative")}
                fit=fit_discriminant(*[[r["features"] for r in panels[k]] for k in ("development_null","development_alternative")])
                coefficients[name]=fit
                results[name]={k:describe(v) for k,v in panels.items()}
            else:
                fit=frozen["coefficients"][name]
                cal={k:panel(ensemble,k,handle,fit) for k in ("calibration_null","calibration_zero")}
                threshold=choose_threshold({k:[r["score"] for r in v] for k,v in cal.items()})
                # Freeze calibration before generating the alternative evaluation panel.
                (output/(name+"-threshold.json")).write_text(json.dumps(threshold,indent=2)+"\n")
                eva={k:panel(ensemble,k,handle,fit) for k in ("evaluation_null","evaluation_zero","evaluation_alternative")}
                results[name]=dict(**threshold,**evaluate_scores({k:[r["score"] for r in v] for k,v in eva.items()},threshold["threshold"]),
                                   panels={k:describe(v) for k,v in dict(**cal,**eva).items()})
    if mode=="develop":
        artifact=dict(source_sha256=source_hashes(),feature_names=P["features"],coefficients=coefficients,
                      development_rows_sha256=sha256(output/"rows.jsonl"))
        (output/"coefficients.json").write_text(json.dumps(artifact,indent=2,allow_nan=False)+"\n")
    result=dict(mode=mode,elapsed_seconds=time.monotonic()-t0,host=platform.node(),
                source_sha256=source_hashes(),coefficients_sha256=expected_sha256,results=results)
    (output/"summary.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("mode",choices=["smoke","develop","evaluate"])
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--coefficients",type=Path)
    parser.add_argument("--expected-coefficients-sha256")
    args=parser.parse_args()
    run(args.mode,args.output,args.coefficients,args.expected_coefficients_sha256)
