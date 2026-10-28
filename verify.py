from pathlib import Path
from playwright.sync_api import sync_playwright
import json, sys
ROOT=Path(__file__).resolve().parent
URL=sys.argv[1] if len(sys.argv)>1 else ROOT.joinpath('index.html').as_uri()
checks=[]
def check(name,fn):
 fn(); checks.append(name); print('PASS',name,flush=True)
def assert_(value,message='assertion failed'):
 assert value,message
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True, channel="chrome")
 context=browser.new_context(accept_downloads=True, reduced_motion="reduce")
 page=context.new_page()
 errors=[]; requests=[]
 page.on('pageerror',lambda err: errors.append(str(err)))
 page.on('request',lambda req: requests.append(req.url))
 page.goto(URL); page.wait_for_load_state('networkidle')
 check('36 lessons / 72 questions / 40 terms embedded',lambda:assert_(page.evaluate('DATA.lessons.length===36 && DATA.lessons.every(l=>l.quiz.length===2) && Object.keys(DATA.glossary).length===40')))
 check('all lessons substantive and references valid',lambda:assert_(page.evaluate('DATA.lessons.every(l=>(l.definition+" "+l.concepts.join(" ")).split(/\\s+/).length>80 && l.scene && l.terms.length===2 && l.technical.length===3 && l.steps.length===3 && l.code.length>100 && l.refs.every(k=>DATA.refs[k]))')))
 page.screenshot(path=str(ROOT/'preview-desktop.png'),full_page=True)
 # Visit every lesson and submit both correct answers using the visible form.
 for id in range(1,37):
  page.goto(URL+'#lesson/'+str(id))
  page.wait_for_selector(f'[data-complete="{id}"]')
  assert page.locator('.quiz').count()==2
  for qi in range(2):
   form=page.locator(f'[data-quiz="{id}-{qi}"]')
   correct=page.evaluate(f'DATA.lessons[{id-1}].quiz[{qi}].answer')
   form.locator(f'input[value="{correct}"]').check()
   form.locator('button').click()
   assert form.locator('.feedback').inner_text().startswith('Correct.')
 check('all 36 routes and all 72 quizzes work',lambda:assert_(page.evaluate('mastery()===36')))
 page.goto(URL+'#lesson/1')
 form=page.locator('[data-quiz="1-0"]');form.locator('input[value="0"]').check();form.locator('button').click()
 check('incorrect answer explains and retry updates mastery',lambda:assert_(form.locator('.feedback').inner_text().startswith('Not quite.') and page.evaluate('mastery()===35')))
 form.locator('input[value="1"]').check();form.locator('button').click()
 page.locator('[data-complete="1"]').click()
 note='A <script> must remain text. Citation support is separate from validity.'
 page.locator('#notes > summary').click();page.locator('#lesson-notes').fill(note)
 page.reload();page.wait_for_selector('#lesson-notes',state='attached')
 check('progress, quiz answers and notes survive reload',lambda:assert_(page.evaluate('done(1) && mastery()===36') and page.locator('#lesson-notes').input_value()==note))
 page.goto(URL+'#projects');page.locator('[data-project="1-0"]').check();page.reload()
 check('project checklist persists',lambda:assert_(page.locator('[data-project="1-0"]').is_checked()))
 page.locator('#search').fill('idempotency');page.wait_for_timeout(250)
 check('global search returns lesson and glossary matches',lambda:assert_(page.locator('.result').count()>=2))
 page.locator('#search').fill('<img src=x onerror=alert(1)>');page.wait_for_timeout(250)
 check('search content safely escaped',lambda:assert_(page.locator('img').count()==0 and page.locator('.empty').count()==1))
 page.goto(URL+'#lab');page.locator('#run-lab').click()
 check('RRF fixture calculation',lambda:assert_('0.032787' in page.locator('#lab-output').inner_text()))
 page.locator('[data-tab="agent"]').click()
 for scenario,expected in [('normal','completed'),('injection','denied'),('loop','budget_exhausted'),('denied','denied')]:
  page.locator('#agent-scenario').select_option(scenario);page.locator('#run-lab').click()
  assert 'TERMINAL: '+expected in page.locator('#lab-output').inner_text()
 check('agent completes, denies injection/tenant access, and bounds loops',lambda:assert_(True))
 page.locator('[data-tab="cost"]').click();page.locator('#run-lab').click()
 check('cost and concurrency calculations',lambda:assert_('$0.003720' in page.locator('#lab-output').inner_text() and '15.00' in page.locator('#lab-output').inner_text()))
 page.locator('#cost-success').fill('101');page.locator('#run-lab').click()
 check('invalid lab inputs rejected',lambda:assert_('Check your inputs' in page.locator('#lab-output').inner_text()))
 page.locator('[data-tab="metrics"]').click();page.locator('#run-lab').click()
 check('retrieval metric calculation',lambda:assert_('RECALL@3: 0.500' in page.locator('#lab-output').inner_text() and '0.500' in page.locator('#lab-output').inner_text()))
 page.goto(URL+'#guide')
 with page.expect_download() as dl:page.locator('#export').click()
 export=ROOT/'test-progress.json';dl.value.save_as(export)
 backup=json.loads(export.read_text())
 check('JSON export contains completed lesson and notes',lambda:assert_(backup['completed']==[1] and backup['notes']['1']==note))
 page.locator('#import').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{"version":2}'})
 check('invalid import preserves current state',lambda:assert_('Import rejected' in page.locator('#import-status').inner_text() and page.evaluate('done(1)')))
 # Reject pathological IDs and invalid values before prompting.
 bad=dict(backup);bad['answers']={'1-0':99}
 page.locator('#import').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':json.dumps(bad).encode()})
 check('invalid quiz backup rejected',lambda:assert_('Import rejected' in page.locator('#import-status').inner_text()))
 page.once('dialog',lambda d:d.accept());page.locator('#reset').click()
 check('reset clears only academy state',lambda:assert_(page.evaluate('state.completed.length===0 && Object.keys(state.notes).length===0')))
 page.once('dialog',lambda d:d.accept());page.locator('#import').set_input_files(export)
 check('valid import restores progress, notes and projects',lambda:assert_(page.evaluate('done(1) && state.projects["1-0"] && mastery()===36') and 'Backup imported' in page.locator('#import-status').inner_text()))
 with page.expect_download() as dl:page.locator('#download-html').click()
 saved=ROOT/'test-offline-copy.html';dl.value.save_as(saved)
 copy=context.new_page();copy.goto(saved.as_uri());copy.wait_for_load_state('networkidle')
 check('downloaded standalone HTML runs independently',lambda:assert_(copy.locator('.hero').count()==1))
 copy.close()
 # Responsive layout across representative pages.
 for width in [390,768,1440]:
  page.set_viewport_size({'width':width,'height':900})
  for route in ['home','curriculum','lesson/7','projects','references','glossary','guide','lab','workshop','review']:
   page.goto(URL+'#'+route)
   assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),f'overflow {width} {route}'
  if width==390:
   page.goto(URL+'#home');page.screenshot(path=str(ROOT/'preview-mobile.png'),full_page=True)
   page.locator('#menu').click();assert page.locator('#menu').get_attribute('aria-expanded')=='true'
   page.locator('[data-nav="curriculum"]').click();page.wait_for_function('document.querySelector("#menu").getAttribute("aria-expanded")==="false"')
 check('responsive layouts and mobile navigation',lambda:assert_(True))
 # Direct file mode must make no external requests.
 if URL.startswith('file:'):
  check('standalone has zero HTTP requests',lambda:assert_(not [u for u in requests if u.startswith('http')]))
 else:
  page.goto(URL+'#guide');page.wait_for_function('cacheStatus.startsWith("Hosted offline cache ready")')
  page.reload();page.wait_for_function('navigator.serviceWorker.controller !== null')
  context.set_offline(True);page.reload();page.wait_for_selector('h1')
  page.goto(URL+'#lesson/36');page.wait_for_selector('[data-complete="36"]')
  check('hosted offline reload and lesson navigation',lambda:assert_(page.locator('h1').inner_text()==page.evaluate('DATA.lessons[35].title')))
  context.set_offline(False)
 check('no JavaScript runtime errors',lambda:assert_(not errors,str(errors)))
 # Storage denial should warn, but not block reading or exporting.
 restricted=browser.new_context()
 restricted.add_init_script('Object.defineProperty(window, "localStorage", {get(){throw new Error("blocked")}})')
 rp=restricted.new_page();rp.goto(URL+'#lesson/1');rp.wait_for_selector('#storage-warning')
 check('storage denial degrades visibly without blocking lessons',lambda:assert_(rp.locator('#storage-warning').is_visible() and rp.locator('h1').count()==1))
 restricted.close();context.close();browser.close()
 report={'mode': 'file' if URL.startswith('file:') else 'hosted','checks':checks,'count':len(checks),'errors':errors}
 (ROOT/('verification-'+report['mode']+'.json')).write_text(json.dumps(report,indent=2))
 export.unlink(missing_ok=True);saved.unlink(missing_ok=True)
 print(json.dumps({'passed':len(checks),'mode':report['mode']}))
