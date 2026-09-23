import json,re,urllib.request,datetime,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
master=ROOT/"data"/"regulatory-master.json"
out=ROOT/"data"/"quarterly-regulatory-audit.json"
data=json.loads(master.read_text())
results=[]
for x in data.get("records",[]):
    url=x.get("source_url")
    r={"active_ingredient":x.get("active_ingredient"),"brand_product":x.get("brand_product"),"source_url":url,
       "source_type":x.get("source_type"),"regulatory_status":x.get("regulatory_status"),
       "checked_at":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    if not url:
        r["status"]="exception-no-current-source"
        results.append(r); continue
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"RheumatologyMedicinesQuarterlyAudit/2.0"})
        html=urllib.request.urlopen(req,timeout=30).read().decode("utf-8","ignore")
        patterns=[
          r"Summary of Product Characteristics last updated on medicines\.ie:\s*([^<\n]+)",
          r"Last updated:\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})",
          r"This page was last updated on\s*([^<\n]+)"
        ]
        observed=None
        for pat in patterns:
            m=re.search(pat,html,re.I)
            if m: observed=m.group(1).strip(); break
        r["observed_update_text"]=observed
        r["status"]="reachable-review-date" if observed else "reachable-manual-review"
    except Exception as e:
        r["status"]="check-failed"; r["error"]=str(e)[:300]
    results.append(r)
summary={
 "generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "policy":"Quarterly regulatory audit only. Never auto-publish prescribing changes. Changed/uncertain records require clinical review before promotion to the live app.",
 "source_hierarchy":data.get("source_hierarchy",[]),
 "results":results
}
out.write_text(json.dumps(summary,indent=2))
print(f"Audited {len(results)} canonical regulatory records; review any failed, changed or manual-review entries before release.")
