import importlib.util, sys, json
sys.argv=["x"]
spec=importlib.util.spec_from_file_location("orc","data/q012-pilot/collapsed_oracle.py"); o=importlib.util.module_from_spec(spec); spec.loader.exec_module(o)
pilot=o.pilot
pts=o.points()
out={}
for name,pe in pts.items():
    row={}
    for forest,(c1,c2) in (("T1_root",([1],[])),("T2_pair",([],[(2,5)]))):
        d=dict(o.D, c1_lin=c1, C1=len(c1), c2_par=[a for a,_ in c2], c2_dau=[b for _,b in c2], C2=len(c2))
        try:
            a=pilot.local_reference(d,pe,800,12.0); b=pilot.local_reference(d,pe,1600,12.0); c=pilot.local_reference(d,pe,1600,16.0)
            qual = abs(a-b)<=1e-6 and abs(c-b)<=1e-6
            ev=o.evaluator(pe,forest,"selection")
            row[forest]=dict(eval_minus_qualified_ref=ev-b, ref_res=a-b, ref_dom=c-b, qualified=qual)
        except Exception as e:
            row[forest]=dict(error=str(e))
    out[name]=row
    print(name, {f:{k:(f"{v:+.1e}" if isinstance(v,float) else v) for k,v in r.items()} for f,r in row.items()})
json.dump(out, open("scratch/oracle_selection_qualified.json","w"), indent=1, default=float)
