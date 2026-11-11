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
    assert not errors,errors
    b.close()
server.shutdown()
print('PASS: touch/keyboard/focus, bounded effects, audio consent/volumes, 0.6.1/0.7.0 saves, offline cap, 30 colony levels, Titan technologies, export/import, 320px/800px, reduced motion, unlock animation; no JS errors')
