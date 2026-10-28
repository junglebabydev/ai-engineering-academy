from pathlib import Path
from playwright.sync_api import sync_playwright
import json,zipfile,subprocess,sys
R=Path(__file__).resolve().parent
URL=sys.argv[1] if len(sys.argv)>1 else (R/'index.html').as_uri()
checks=[]
def check(name,condition):
 assert condition,name
 checks.append(name);print('PASS',name,flush=True)
legacy={'version':1,'completed':[1,7],'answers':{'1-0':1},'notes':{'7':'Earlier note <script> stays text.'},'projects':{'1-0':True},'lastLesson':7}
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,channel='chrome');c=b.new_context(accept_downloads=True,reduced_motion='reduce');page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL);page.evaluate('(x)=>localStorage.setItem(KEY,JSON.stringify(x))',legacy);page.reload()
 check('earlier progress archived without marking new content complete',page.evaluate('state.edition===2 && state.completed.length===0 && mastery()===0 && state.legacy.completed.length===2'))
 page.goto(URL+'#guide');page.get_by_text('Read earlier lesson notes',exact=True).click();check('earlier notes readable and safely escaped','Earlier note <script>' in page.locator('body').inner_text() and page.locator('#main script').count()==0)
 with page.expect_download() as dl:page.locator('#export-legacy').click()
 path=R/'test-legacy.json';dl.value.save_as(path);check('earlier-edition JSON export preserves original notes',json.loads(path.read_text())['notes']==legacy['notes']);path.unlink()
 page.goto(URL+'#lesson/7');page.locator('#activity-response').fill('My activity attempt <img src=x>');page.locator('#recall-response').fill('Facts need sources and dates.')
 page.reload();check('activity and recall writing survive reload',page.locator('#activity-response').input_value()=='My activity attempt <img src=x>' and page.locator('#recall-response').input_value()=='Facts need sources and dates.')
 check('technical depth and answers begin collapsed',not page.locator('#technical').evaluate('(e)=>e.open') and not page.locator('#exercise + .lab-box details').evaluate('(e)=>e.open'))
 page.locator('[data-complete="7"]').click();page.goto(URL+'#review');check('recall practice uses completed lessons and saved writing','Facts need sources' in page.locator('textarea[data-recall="7"]').input_value())
 page.goto(URL+'#workshop');page.locator('#workshop-form button').click();text=page.locator('#workshop-output').inner_text()
 check('workshop enforces age/price and retains unknown availability','SWIM-01' in text and 'SWIM-02' not in text and 'SWIM-03' not in text and 'unverified availability' in text)
 page.locator('#parent-age').fill('');page.locator('#workshop-form button').click();check('missing age asks rather than guesses','clarification_needed' in page.locator('#workshop-output').inner_text())
 page.locator('#parent-age').fill('5');page.locator('#parent-budget').fill('20');page.locator('#workshop-form button').click();check('strict low budget produces no match','TERMINAL: no_matches' in page.locator('#workshop-output').inner_text())
 page.locator('#parent-budget').fill('50');page.locator('#parent-interest').select_option('art');page.locator('#workshop-form button').click();text=page.locator('#workshop-output').inner_text();check('unknown price not silently treated as free','ART-01' in text and 'ART-03' not in text)
 for scenario,expected in [('unavailable','tool_unavailable'),('injection','TERMINAL: denied')]:
  page.locator('#parent-scenario').select_option(scenario);page.locator('#workshop-form button').click();check('workshop '+scenario,expected in page.locator('#workshop-output').inner_text())
 with page.expect_download() as dl:page.locator('[data-build-download]').click()
 pack=R/'test-build-pack.zip';dl.value.save_as(pack)
 with zipfile.ZipFile(pack) as z:
  check('offline ZIP is structurally valid with complete build materials',z.testzip() is None and {'BUILD-GUIDE.md','AGENT-BRIEF.md','activities.csv','parent-tests.csv','search-activities.js','get-activity-details.js','catalogue.json'}<=set(z.namelist()))
  for name in z.namelist():assert z.read(name).decode()==(R/'agent-build-pack'/name).read_text(),name
 pack.unlink()
 with page.expect_download() as dl:page.locator('[data-catalogue-download]').click()
 csv=R/'test-activities.csv';dl.value.save_as(csv);check('catalogue CSV matches supplied version',csv.read_text()==(R/'agent-build-pack/activities.csv').read_text());csv.unlink()
 # New backup contains answers, worksheets, recall, and legacy archive.
 page.goto(URL+'#guide')
 with page.expect_download() as dl:page.locator('#export').click()
 backup=R/'test-new-progress.json';dl.value.save_as(backup);saved=json.loads(backup.read_text());check('new export preserves learning work and earlier archive',saved['edition']==2 and saved['activities']['7'].startswith('My activity') and saved['legacy']['notes']==legacy['notes'])
 page.once('dialog',lambda d:d.accept());page.locator('#reset').click();page.once('dialog',lambda d:d.accept());page.locator('#import').set_input_files(backup);check('new edition import round-trip',page.evaluate('state.completed.includes(7) && state.recall[7]==="Facts need sources and dates." && state.legacy.notes[7].includes("Earlier note")'))
 # A still-open earlier edition tab cannot erase newly saved worksheets.
 other=c.new_page();other.goto(URL);other.evaluate('(x)=>localStorage.setItem(KEY,JSON.stringify(x))',legacy)
 page.wait_for_function('JSON.parse(localStorage.getItem(KEY)).edition===2')
 check('earlier-tab saves do not erase new worksheets',page.evaluate('state.activities[7].startsWith("My activity") && JSON.parse(localStorage.getItem(KEY)).activities[7].startsWith("My activity")'))
 other.close()
 # Malformed writing map must not replace state.
 invalid={**saved,'activities':{'__proto__':'bad'}};page.locator('#import').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':json.dumps(invalid).encode()});check('invalid writing keys rejected','Import rejected' in page.locator('#import-status').inner_text() and page.evaluate('state.completed.includes(7)'))
 backup.unlink()
 # Old backup import archives and explicitly restarts rewritten quiz/completion state.
 page.once('dialog',lambda d:d.accept());page.locator('#import').set_input_files({'name':'earlier.json','mimeType':'application/json','buffer':json.dumps(legacy).encode()});check('earlier backup import archives rather than inventing mastery',page.evaluate('state.completed.length===0 && state.legacy.completed.length===2 && mastery()===0'))
 for width in [390,768,1440]:
  page.set_viewport_size({'width':width,'height':900})
  for route in ['home','lesson/1','lesson/18','lesson/33','workshop','projects','review','guide']:
   page.goto(URL+'#'+route);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,route)
 page.set_viewport_size({'width':1440,'height':1000});page.goto(URL+'#lesson/1');page.locator('#main').evaluate('(e)=>e.blur()');page.screenshot(path=str(R/'preview-beginner-lesson.png'),full_page=True)
 page.set_viewport_size({'width':390,'height':844});page.goto(URL+'#workshop');page.locator('#main').evaluate('(e)=>e.blur()');page.screenshot(path=str(R/'preview-beginner-mobile.png'))
 check('new views fit phone/tablet/desktop',True)
 check('new teaching interactions produce no runtime errors',not errors)
 c.close();b.close()
# Verify supplied n8n glue using a simulated n8n input object, with no remote calls.
runner=r'''
const fs = require('fs');
const run = (file,input) => new Function('$input',fs.readFileSync(file,'utf8'))({first:()=>({json:input})})[0].json;
let r=run('agent-build-pack/search-activities.js',{ageYears:5,budgetMaxSGD:50,interest:'swimming',district:'Bukit Timah'});
if(r.status!=='success'||r.matches.map(x=>x.id).join()!=='SWIM-01')throw Error('known search');
for(const age of ['',null,'wrong',-1]){if(run('agent-build-pack/search-activities.js',{ageYears:age,budgetMaxSGD:50}).status!=='invalid_input')throw Error('age bounds');}
if(run('agent-build-pack/search-activities.js',{ageYears:5,budgetMaxSGD:20,interest:'swimming',district:'Bukit Timah'}).status!=='no_matches')throw Error('no match');
if(run('agent-build-pack/search-activities.js',{ageYears:5,budgetMaxSGD:50,interest:'art',district:'Bukit Timah'}).matches.some(x=>x.priceSGD===null))throw Error('unknown price');
if(run('agent-build-pack/search-activities.js',{ageYears:5,budgetMaxSGD:50,interest:'swimming',district:'unknown'}).status!=='invalid_input')throw Error('district broadening');
if(run('agent-build-pack/get-activity-details.js',{activityId:'not-real'}).status!=='not_found')throw Error('invented ID');
if(run('agent-build-pack/get-activity-details.js',{activityId:'SWIM-01'}).activity.availability!=='unverified')throw Error('availability');
'''
r=subprocess.run(['node','-e',runner],cwd=R,capture_output=True,text=True);check('supplied n8n scripts pass known-match, missing/invalid input, no-match, unknown-price, scope and ID tests',r.returncode==0)
report={'edition':2,'url':URL,'count':len(checks),'checks':checks,'scope':'Browser simulation and supplied Code-node logic. Live n8n/model wiring is not exercised.'}
(R/'verification-beginner.json').write_text(json.dumps(report,indent=2));print(json.dumps({'passed':len(checks)}))
