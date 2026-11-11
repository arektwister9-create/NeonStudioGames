"""Capture real game screens and render store exports at Google Play sizes."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from threading import Thread
from playwright.sync_api import sync_playwright
import json,base64,shutil,os
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'store-assets';OUT.mkdir(exist_ok=True)
META=ROOT/'fastlane/metadata/android/pl-PL/images';(META/'phoneScreenshots').mkdir(parents=True,exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT/'app/src/main/assets')));Thread(target=server.serve_forever,daemon=True).start()
icon=base64.b64encode((ROOT/'app/src/main/res/mipmap-xxxhdpi/ic_launcher.png').read_bytes()).decode()
NOW=1800000000000
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.environ.get('NEON_CHROMIUM') or shutil.which('chromium') or p.chromium.executable_path,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':512,'height':512},device_scale_factor=1)
 page.set_content('<html><body style="margin:0;background:#050816"><img style="display:block;width:512px;height:512px" src="data:image/png;base64,'+icon+'"></body></html>');page.screenshot(path=str(OUT/'icon-512.png'));page.close()
 page=browser.new_page(viewport={'width':1024,'height':500},device_scale_factor=1)
 page.set_content('''<html><style>*{box-sizing:border-box}body{margin:0;width:1024px;height:500px;overflow:hidden;color:#eef8ff;background:radial-gradient(ellipse at 80% 50%,#38245d,#071024 65%);font-family:Arial,sans-serif}.stars{position:absolute;inset:0;background:radial-gradient(circle at 15% 20%,#8deeff 0 1px,transparent 2px),radial-gradient(circle at 55% 80%,#ff8cec 0 1px,transparent 2px);background-size:95px 120px,117px 100px}.copy{position:absolute;left:56px;top:75px}.brand{color:#58efff;font-size:17px;letter-spacing:5px;font-weight:bold}h1{font-size:76px;line-height:1;margin:23px 0 22px;letter-spacing:2px}h1 span{color:#70f1ff}p{font-size:24px;line-height:1.5;color:#b9d0ee;margin:0}.tag{margin-top:22px;color:#ffe19c;font-size:17px;letter-spacing:2px}img{position:absolute;right:38px;top:75px;width:350px;height:350px;mix-blend-mode:screen}</style><body><div class="stars"></div><div class="copy"><div class="brand">NEON GAMES STUDIO</div><h1>NEON<br><span>EMPIRE</span></h1><p>Obudź rdzeń. Zbuduj imperium.</p><div class="tag">30 POZIOMÓW • 6 SEKTORÓW • OFFLINE</div></div><img src="data:image/png;base64,'''+icon+'"></body></html>')
 page.screenshot(path=str(OUT/'feature-graphic-1024x500.png'));page.close()
 base={'version':5,'energy':6800000,'total':16000000,'taps':530,'levels':{'drone':12,'solar':8,'server':5,'reactor':2,'portal':1},'planets':{'luna':True,'mars':True,'titan':True},'colonies':{'luna':7,'mars':6,'titan':5},'research':{'overclock':True,'fusion':True},'technologies':{'lattice':True,'resonance':True},'coreCampaign':{'chapter':3,'pulses':8},'expedition':{'cleared':14,'materials':18,'modules':{'dock':3,'lab':3,'shield':2}},'last':NOW}
 captures=[('01-operacja-rdzenia.png','combat'),('02-rozbudowa-stacji.png','station'),('03-kolonie.png','planets'),('04-synchronizacja.png','campaign')]
 for filename,mode in captures:
  context=browser.new_context(viewport={'width':360,'height':640},device_scale_factor=3,has_touch=True)
  page=context.new_page();page.add_init_script('Date.now=()=>'+str(NOW)+';localStorage.setItem("neonEmpireSave",'+json.dumps(json.dumps(base))+');');page.goto(f'http://127.0.0.1:{server.server_port}')
  if mode=='combat':page.locator('#startExpedition').click();target='.expedition-hud'
  elif mode=='station':page.locator('.star-map').evaluate('e=>e.open=true');target='.station-panel'
  elif mode=='planets':target='.galaxy-card'
  else:
   page.locator('#legacyCampaign').evaluate('e=>e.open=true');page.locator('#beginSync').click();target='.core-quest'
  page.evaluate('(selector)=>scrollTo(0,document.querySelector(selector).getBoundingClientRect().top+scrollY-8)',target)
  page.wait_for_timeout(450);page.screenshot(path=str(OUT/filename));shutil.copy2(OUT/filename,META/'phoneScreenshots'/filename);context.close()
 shutil.copy2(OUT/'icon-512.png',META/'icon.png');shutil.copy2(OUT/'feature-graphic-1024x500.png',META/'featureGraphic.png');browser.close()
server.shutdown();print('Store icon 512x512, feature graphic 1024x500 and 4 real-game phone screenshots 1080x1920 prepared')
