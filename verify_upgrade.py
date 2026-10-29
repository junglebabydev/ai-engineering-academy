"""Check a real edition-1 worker/storage upgrade. Requires this repository's history."""
from pathlib import Path
import subprocess,tempfile,sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
BASE='b30aab4769214a574bfe8e638b295eae9a88b7eb'
origin=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8081/'
with tempfile.TemporaryDirectory(prefix='.qa-upgrade-',dir=R) as tmp:
 folder=Path(tmp)
 for name in ['index.html','sw.js']:
  folder.joinpath(name).write_bytes(subprocess.check_output(['git','show',f'{BASE}:{name}'],cwd=R))
 url=origin+folder.name+'/'
 with sync_playwright() as p:
  b=p.chromium.launch(headless=True,channel='chrome');c=b.new_context();page=c.new_page();page.goto(url+'#guide')
  page.wait_for_function('cacheStatus.startsWith("Hosted offline cache ready")');page.reload(wait_until='domcontentloaded');page.wait_for_function('navigator.serviceWorker.controller!==null')
  page.evaluate('localStorage.setItem(KEY, JSON.stringify({version:1,completed:[1],answers:{"1-0":1},notes:{"1":"Saved before upgrade"},projects:{},lastLesson:1}))')
  for name in ['index.html','sw.js']:folder.joinpath(name).write_bytes((R/name).read_bytes())
  page.evaluate('navigator.serviceWorker.getRegistration().then(r=>r.update())')
  page.wait_for_function('Promise.all([caches.keys(),navigator.serviceWorker.getRegistration()]).then(([keys,r])=>keys.some(k=>k.endsWith(":3")) && !r.installing && !r.waiting && r.active?.state==="activated")')
  page.reload(wait_until='domcontentloaded');page.wait_for_function('DATA.edition===2')
  assert page.evaluate('state.completed.length===0 && state.legacy.notes[1]==="Saved before upgrade"')
  page.evaluate('state.activities[1]="New worksheet";persist()')
  c.set_offline(True);page.reload(wait_until='domcontentloaded');page.wait_for_selector('h1')
  assert page.evaluate('DATA.edition===2 && state.activities[1]==="New worksheet" && state.legacy.notes[1]==="Saved before upgrade"')
  c.close();b.close()
report={'edition':2,'checks':['Edition-1 worker and stored notes upgrade to edition 2','New completion starts fresh and earlier notes remain archived','New edition and worksheets reload offline after upgrade'],'count':3}
(R/'verification-upgrade.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
