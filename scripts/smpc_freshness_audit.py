import json,re,urllib.request,datetime,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
registry=ROOT/"data"/"smpc-source-registry.json"
out=ROOT/"data"/"smpc-audit.json"
sources=json.loads(registry.read_text())
results=[]
for x in sources:
    r=dict(x); r["checked_at"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        req=urllib.request.Request(x["url"],headers={"User-Agent":"RheumatologyMedicinesSmPCAudit/1.0"})
        html=urllib.request.urlopen(req,timeout=30).read().decode("utf-8","ignore")
        m=re.search(r"(?:Summary of Product Characteristics last updated on medicines\.ie:|Updated on)\s*([0-9]{1,2}[/ ][0-9A-Za-z]+[/ ][0-9]{4})",html,re.I)
        current=m.group(1) if m else None
        r["observed_revision"]=current
        r["status"]="changed-review-required" if current and x.get("known_revision") and current!=x["known_revision"] else ("ok" if current else "manual-review")
    except Exception as e:
        r["status"]="check-failed"; r["error"]=str(e)[:300]
    results.append(r)
out.write_text(json.dumps({"generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"results":results},indent=2))
if any(x["status"]=="changed-review-required" for x in results):
    print("SmPC change detected: clinical re-verification required.")
