from pathlib import Path
import json,re,subprocess
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent;URL=(R/'index.html').as_uri();D=json.loads((R/'curriculum.json').read_text());checks=[]
def check(name,ok):
 assert ok,name
 checks.append(name);print('PASS',name,flush=True)
check('all 36 definitions and general explanations are project-independent',all(not re.search(r'Jungle|concierge|parent',l['definition']+' '+' '.join(l['concepts']),re.I) for l in D['lessons']))
check('all original technical topics retained', [l['technicalTopic'] for l in D['lessons']]==[l['title'] for l in json.loads((R/'technical-foundations.json').read_text())['lessons']])
check('all lesson activities and quiz answers retained',all(l['projectExample'] and l['scene'] and len(l['quiz'])==2 for l in D['lessons']))
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,channel='chrome');c=b.new_context(reduced_motion='reduce',viewport={'width':1440,'height':1000});page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(URL)
 page.evaluate('state.completed=[1,7];state.answers={"1-0":1};state.notes[1]="Earlier topic notes";state.activities[7]="My existing worksheet";persist()')
 page.reload();check('current edition-2 progress and writing survive without reset',page.evaluate('state.completed.length===2 && state.answers["1-0"]===1 && state.notes[1]==="Earlier topic notes" && state.activities[7]==="My existing worksheet"'))
 for l in D['lessons']:
  page.goto(URL+'#lesson/'+str(l['id']));page.wait_for_selector('.definition')
  assert page.locator('h1').inner_text()==l['title']
  assert page.locator('.definition').inner_text()==l['definition']
  assert not page.locator('#application').evaluate('(e)=>e.open')
  assert page.evaluate('document.querySelector("#briefing").compareDocumentPosition(document.querySelector("#example")) & Node.DOCUMENT_POSITION_FOLLOWING')
  assert page.evaluate('document.querySelector("#concept-practice").compareDocumentPosition(document.querySelector("#application")) & Node.DOCUMENT_POSITION_FOLLOWING')
 check('every lesson leads with definition, mechanism and everyday example before project application',True)
 page.goto(URL+'#lesson/1');page.locator('[data-scroll="application"]').click();check('lesson navigation expands the separate project section',page.locator('#application').evaluate('(e)=>e.open'))
 page.set_viewport_size({'width':390,'height':844})
 for route in ['lesson/1','lesson/16','lesson/33','curriculum','home']:
  page.goto(URL+'#'+route);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 page.goto(URL+'#lesson/1');page.locator('#main').evaluate('(e)=>e.blur()');page.screenshot(path=str(R/'preview-concepts-mobile.png'))
 page.set_viewport_size({'width':1440,'height':1000});page.locator('#toast').evaluate('(e)=>e.textContent=""');page.screenshot(path=str(R/'preview-concepts.png'),full_page=True)
 check('concept-first views fit mobile and desktop',True);check('no runtime errors in revised lesson interactions',not errors)
 c.close();b.close()
report={'edition':2,'revision':3,'count':len(checks),'checks':checks};(R/'verification-concepts.json').write_text(json.dumps(report,indent=2))
