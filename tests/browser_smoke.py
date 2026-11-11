"""Run with Python Playwright and installed Chromium; serves local assets itself."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import os, json, math, shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('NEON_TEST_OUTPUT','/tmp/neon-071-tests'));OUT.mkdir(parents=True,exist_ok=True)
class Handler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT/'app/src/main/assets')))
Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}'
NOW=1800000000000
legacy={'version':5,'energy':99,'total':250000,'taps':101,'levels':{'drone':2,'solar':1,'server':0,'reactor':0,'portal':0},'research':{'overclock':True},'planets':{'luna':True,'mars':True,'titan':True},'missions':{'first':True},'daily':{'lastClaim':'2026-01-01','streak':4},'achievements':{'energy1k':True},'last':NOW}
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,executable_path=os.environ.get('NEON_CHROMIUM') or shutil.which('chromium') or p.chromium.executable_path,args=['--no-sandbox'])
    errors=[]
    def open_game(save=None,width=390):
        context=b.new_context(viewport={'width':width,'height':844},has_touch=True)
        page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        init='Date.now=()=>'+str(NOW)+';'
        if save is not None:init+='localStorage.setItem("neonEmpireSave",'+json.dumps(json.dumps(save))+');'
        page.add_init_script(init);page.goto(url);page.wait_for_selector('#coreName')
        return context,page
    c,page=open_game()
    assert page.evaluate('window.NeonAudio.getPreferences().musicConsent') is False
    assert page.evaluate('getComputedStyle(document.querySelector("#tap")).webkitTapHighlightColor')=='rgba(0, 0, 0, 0)'
    page.locator('#tap').tap();assert page.locator('#energy').inner_text()=='1'
    page.locator('#tap').focus();page.keyboard.press('Space');assert page.locator('#energy').inner_text()=='2'
    assert page.locator('#tap').evaluate('e=>getComputedStyle(e).outlineStyle')=='solid'
    for _ in range(24):page.locator('#tap').dispatch_event('click')
    assert page.locator('.core-burst').count()<=8
    page.wait_for_timeout(900);assert page.locator('.core-burst').count()==0
    page.locator('#menuToggle').click()
    page.locator('#musicToggle').click();page.wait_for_timeout(200)
    assert page.evaluate('window.NeonAudio.getPreferences().musicConsent') is True
    page.locator('#musicVolume').fill('31');page.locator('#effectsVolume').fill('72')
    prefs=page.evaluate('JSON.parse(localStorage.getItem("neonEmpireAudio"))')
    assert prefs['musicVolume']==.31 and prefs['effectsVolume']==.72
    page.locator('#musicToggle').click();assert page.locator('#musicToggle').get_attribute('aria-pressed')=='false'
    page.screenshot(path=str(OUT/'audio-settings.png'),full_page=True)
    before_policy=page.locator('#energy').inner_text()
    page.locator('.privacy-link').click();assert 'arektwister9@gmail.com' in page.locator('body').inner_text()
    page.locator('a[href="index.html"]').click();assert page.locator('#energy').inner_text()==before_policy
    c.close()
    for version in ['0.6.1','0.7.0']:
        c,page=open_game(legacy)
        page.locator('#saveBtn').evaluate('e=>e.click()')
        saved=page.evaluate('JSON.parse(localStorage.getItem("neonEmpireSave"))')
        for key in ['energy','total','taps','levels','research','planets','missions','daily','achievements','version']:assert saved[key]==legacy[key],(version,key,saved[key])
        assert saved['colonies']=={'luna':1,'mars':1,'titan':1}
        expected=(7+20)*1.25*1.85*1.08
        assert page.locator('#rate').inner_text()==str(math.floor(expected))
        c.close()
    offline=dict(legacy,last=NOW-12*3600000)
    c,page=open_game(offline);page.locator('#saveBtn').evaluate('e=>e.click()');saved=page.evaluate('JSON.parse(localStorage.getItem("neonEmpireSave"))')
    assert abs(saved['energy']-(99+28800*expected))<.0001
    c.close()
    rich=dict(legacy,energy=1e12,total=1e12)
    c,page=open_game(rich,width=320)
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    for planet in ['luna','mars','titan']:
        for level in range(2,11):
            page.locator(f'[data-planet="{planet}"] [data-action="build"]').click()
            assert page.locator(f'[data-planet="{planet}"]').get_attribute('data-colony')==str(level)
        assert page.locator(f'[data-planet="{planet}"] [data-action="build"]').is_disabled()
    for tech in ['lattice','resonance','vacuum','heart']:page.locator(f'[data-tech="{tech}"]').click()
    page.locator('#saveBtn').evaluate('e=>e.click()');saved=page.evaluate('JSON.parse(localStorage.getItem("neonEmpireSave"))')
    assert saved['colonies']=={'luna':10,'mars':10,'titan':10}
    assert len(saved['technologies'])==4
    assert saved['total']==rich['total']
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.screenshot(path=str(OUT/'max-colonies-320px.png'),full_page=True)
    # Export/import round trip includes new progression and remains JSON version 5.
    page.evaluate('window.__exported=null;window.NeonEmpireAndroid={exportSave:x=>window.__exported=x}')
    page.locator('#exportBtn').evaluate('e=>e.click()');exported=page.evaluate('window.__exported')
    page.locator('#importFile').set_input_files({'name':'save.json','mimeType':'application/json','buffer':exported.encode()})
    assert page.locator('[data-planet="titan"]').get_attribute('data-colony')=='10'
    page.context.set_offline(True);before=page.locator('#energy').inner_text();page.locator('#tap').dispatch_event('click');page.locator('#saveBtn').evaluate('e=>e.click()')
    assert page.evaluate('JSON.parse(localStorage.getItem("neonEmpireSave")).taps')==rich['taps']+1
    page.context.set_offline(False)
    page.wait_for_timeout(900);page.emulate_media(reduced_motion='reduce');page.locator('#tap').dispatch_event('click');assert page.locator('.core-burst').count()==0
    c.close()
    # Actual planet unlock, construction visual and evolution from a threshold.
    unlocked=dict(legacy,planets={},total=999,energy=1e6)
    c,page=open_game(unlocked,width=800)
    page.locator('#tap').tap();page.locator('[data-planet="luna"] [data-action="unlock"]').click()
    assert page.locator('[data-planet="luna"]').get_attribute('data-colony')=='1'
    assert page.locator('[data-planet="luna"] .colony-unlock').count()==1
    page.screenshot(path=str(OUT/'unlock-and-core.png'),full_page=True)
    c.close()
    # First campaign loop: real charge, pulse, wrong node, correct sync, durable reward.
    journey=dict(legacy,energy=1000,total=1000,planets={},levels={'drone':3,'solar':0,'server':0,'reactor':0,'portal':0})
    c,page=open_game(journey)
    page.locator('#legacyCampaign > summary').click()
    assert page.locator('#beginSync').is_disabled()
    page.locator('#campaignGoals .goal-link').first.click();assert page.locator('#tap').evaluate('e=>e===document.activeElement');assert page.locator('#tap').get_attribute('tabindex')!='-1'
    for _ in range(12):page.locator('#tap').dispatch_event('click')
    assert page.locator('#releasePulse').is_enabled()
    page.locator('#releasePulse').click()
    assert page.locator('#releasePulse').is_disabled()
    assert page.locator('#beginSync').is_enabled()
    page.locator('#beginSync').click()
    page.locator('[data-node="1"]').click()
    assert 'nie tracisz' in page.locator('#syncStatus').inner_text()
    for node in [0,2,1]:page.locator('[data-node="'+str(node)+'"]').click()
    assert page.locator('#campaignTitle').inner_text()=='Latarnia Luna-9'
    saved=page.evaluate('JSON.parse(localStorage.getItem("neonEmpireSave"))')
    assert saved['coreCampaign']['chapter']==1 and saved['coreCampaign']['pulses']==1
    assert saved['coreCampaign']['charge']==0
    page.screenshot(path=str(OUT/'first-fragment.png'),full_page=True)
    c.close()
    # Final campaign objective and genuine last sequence open the persistent gate.
    finale=dict(legacy,energy=1e8,total=1e8,colonies={'luna':10,'mars':10,'titan':10},technologies={'lattice':True,'resonance':True,'heart':True},coreCampaign={'chapter':5,'pulses':17,'charge':9})
    c,page=open_game(finale,width=390)
    page.locator('#legacyCampaign > summary').click()
    page.locator('#tap').dispatch_event('click');page.locator('#releasePulse').click();page.locator('#beginSync').click()
    for node in [1,2,0,2,1,0]:page.locator('[data-node="'+str(node)+'"]').click()
    assert page.locator('#coreStage').evaluate('e=>e.classList.contains("gate-open")')
    assert page.locator('#campaignEnding').is_visible()
    assert page.locator('#beginSync').is_hidden()
    assert page.evaluate('JSON.parse(localStorage.getItem("neonEmpireSave")).coreCampaign.chapter')==6
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.screenshot(path=str(OUT/'gate-open.png'),full_page=True)
    c.close()
    # Play real encounters through visible controls and build a visible dock.
    c,page=open_game()
    page.locator('#startExpedition').click();assert page.locator('#tap').is_disabled()
    page.locator('[data-target]').first.click()
    page.evaluate("""window.finishOperation=()=>{let steps=0;while(document.querySelector('[data-target]')&&steps++<300){let target=document.querySelector('[data-target]');const tool=[0,1,2].find(i=>target.classList.contains('target-'+i));document.querySelector('[data-tool="'+tool+'"]').click();document.querySelector('[data-target]').click()}if(steps>=300)throw Error('Encounter stalled')};window.finishOperation()""")
    assert page.locator('#expeditionLevel').inner_text()=='POZIOM 2 / 30'
    assert '2 MATERIAŁÓW' in page.locator('#stationMaterials').inner_text()
    page.locator('[data-building-upgrade="dock"]').click()
    assert page.locator('[data-building="dock"]').get_attribute('data-level')=='1'
    assert page.locator('[data-building="dock"] .building-model i').count()==1
    assert page.locator('#stationOrbit .orbital-dock').count()==1
    page.screenshot(path=str(OUT/'station-first-dock.png'),full_page=True)
    # Reach scanner, use a wrong tool, preserve the active encounter through import.
    page.locator('#startExpedition').click();page.evaluate('window.finishOperation()')
    page.locator('#startExpedition').click()
    tool=page.locator('[data-target]').first.evaluate("e=>[0,1].find(i=>e.classList.contains('target-'+i))")
    page.locator('[data-tool="'+str(1-tool)+'"]').click();page.locator('[data-target]').first.click()
    assert 'OSŁONA 4 / 6' in page.locator('#expeditionHealth').inner_text()
    state=page.evaluate('localStorage.getItem("neonEmpireSave")')
    page.locator('#importFile').set_input_files({'name':'active.json','mimeType':'application/json','buffer':state.encode()})
    assert 'OSŁONA 4 / 6' in page.locator('#expeditionHealth').inner_text()
    before_repair=page.evaluate('JSON.parse(localStorage.getItem("neonEmpireSave"))')
    page.locator('#repairExpedition').click();assert 'OSŁONA 6 / 6' in page.locator('#expeditionHealth').inner_text()
    after_repair=page.evaluate('JSON.parse(localStorage.getItem("neonEmpireSave"))')
    assert after_repair['energy']==before_repair['energy']-100 and after_repair['total']==before_repair['total']
    page.evaluate('window.finishOperation()')
    for _ in range(2):page.locator('#startExpedition').click();page.evaluate('window.finishOperation()')
    assert page.locator('#coreStage').get_attribute('data-sector')=='1'
    assert page.evaluate('JSON.parse(localStorage.getItem("neonEmpireSave")).expedition.cleared')==5
    page.screenshot(path=str(OUT/'sector-two.png'),full_page=True)
    c.close()
    # Final sector and completed station are visibly distinct from the starting camp.
    endgame=dict(legacy,expedition={'cleared':29,'materials':20,'modules':{'dock':6,'lab':6,'shield':6}})
    c,page=open_game(endgame,width=320)
    assert page.locator('#coreStage').get_attribute('data-sector')=='5'
    assert page.locator('#coreName').inner_text()=='IMPERIUM GALAKTYCZNE'
    page.locator('#startExpedition').click()
    page.screenshot(path=str(OUT/'guardian-active-320px.png'),full_page=True)
    page.locator('#coreStage').screenshot(path=str(OUT/'guardian-playfield.png'))
    page.evaluate("""let steps=0;while(document.querySelector('[data-target]')&&steps++<200){const target=document.querySelector('[data-target]');const tool=[0,1,2].find(i=>target.classList.contains('target-'+i));document.querySelector('[data-tool="'+tool+'"]').click();document.querySelector('[data-target]').click()}if(steps>=200)throw Error('Finale stalled')""")
    assert 'UKOŃCZONO' in page.locator('#expeditionLevel').inner_text()
    assert page.evaluate('JSON.parse(localStorage.getItem("neonEmpireSave")).expedition.cleared')==30
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.screenshot(path=str(OUT/'galactic-station-320px.png'),full_page=True)
    page.locator('#coreStage').screenshot(path=str(OUT/'complete-core-playfield.png'))
    c.close()
    c,page=open_game(width=1280)
    page.set_viewport_size({'width':1280,'height':720});page.locator('#tap').click();page.locator('#startExpedition').click();page.locator('[data-target]').first.click()
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    c.close()
    assert not errors,errors
    b.close()
server.shutdown()
print('PASS: touch/keyboard/focus, bounded effects, audio consent/volumes, 0.6.1/0.7.0 saves, offline cap, 30 colony levels, Titan technologies, export/import, 320px/800px, reduced motion, unlock animation, campaign charging/sync/retry/rewards and final gate; expeditions, tool errors, construction, save/import during combat, sector transition and level 30; no JS errors')
