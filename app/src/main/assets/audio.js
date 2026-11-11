/* Original procedural score: slow minor/add9 pads and sparse high-register stars.
   No recordings, samples, external assets or pre-existing melodies. */
(()=>{'use strict';
const KEY='neonEmpireAudio',defaults={musicConsent:false,musicVolume:.25,effectsVolume:.55};
let prefs={...defaults};try{const x=JSON.parse(localStorage.getItem(KEY));if(x&&typeof x==='object'){prefs.musicConsent=x.musicConsent===true;for(const k of ['musicVolume','effectsVolume'])if(Number.isFinite(x[k]))prefs[k]=Math.max(0,Math.min(1,x[k]))}}catch(_){}
let ctx,music,effects,compressor,timer=null,nextBar=0,bar=0,activeVoices=0,lastClick=-Infinity,started=false;
const musicVoices=new Set();
function store(){try{localStorage.setItem(KEY,JSON.stringify(prefs))}catch(_){}}
function context(){
 if(ctx)return ctx;
 const Audio=window.AudioContext||window.webkitAudioContext;if(!Audio)return null;
 try{ctx=new Audio();music=ctx.createGain();effects=ctx.createGain();compressor=ctx.createDynamicsCompressor();compressor.threshold.value=-18;compressor.ratio.value=4;music.connect(compressor);effects.connect(compressor);compressor.connect(ctx.destination);music.gain.value=prefs.musicVolume;effects.gain.value=prefs.effectsVolume;return ctx}catch(_){return null}
}
function tone(freq,time,duration,volume,bus,type='sine'){
 if(!ctx||activeVoices>=40)return;
 const o=ctx.createOscillator(),g=ctx.createGain();o.type=type;o.frequency.setValueAtTime(freq,time);
 g.gain.setValueAtTime(0,time);g.gain.linearRampToValueAtTime(volume,time+Math.min(.15,duration*.15));g.gain.exponentialRampToValueAtTime(.0001,time+duration);
 o.connect(g);g.connect(bus);activeVoices++;if(bus===music)musicVoices.add(o);
 o.onended=()=>{o.disconnect();g.disconnect();activeVoices--;musicVoices.delete(o)};o.start(time);o.stop(time+duration+.02);
}
const chords=[[45,52,59,64],[41,48,55,60],[48,55,62,67],[43,50,57,62]],hz=m=>440*Math.pow(2,(m-69)/12);
function schedule(){
 if(!ctx||ctx.state!=='running'||!prefs.musicConsent||prefs.musicVolume===0||document.hidden)return;
 while(nextBar<ctx.currentTime+.4){const chord=chords[bar%chords.length];chord.forEach((note,i)=>tone(hz(note),nextBar+i*.07,7.8,.055,music,'sine'));tone(hz(chord[0]-12),nextBar,7.9,.04,music);tone(hz(chord[(bar*3+1)%4]+24),nextBar+2.2,2.4,.035,music);tone(hz(chord[(bar+2)%4]+12),nextBar+5.1,2.5,.025,music,'triangle');nextBar+=8;bar++}
}
function stopMusic(){if(timer!==null)clearInterval(timer);timer=null;for(const o of musicVoices){try{o.stop()}catch(_){}}musicVoices.clear()}
function startMusic(){if(!ctx||document.hidden||!prefs.musicConsent||prefs.musicVolume===0)return;stopMusic();nextBar=ctx.currentTime+.06;schedule();timer=setInterval(schedule,200)}
async function gesture(){
 if(document.hidden||(!prefs.musicConsent&&prefs.effectsVolume===0))return;
 const c=context();if(!c)return;
 started=true;try{if(c.state==='suspended')await c.resume();if(prefs.musicConsent&&timer===null)startMusic()}catch(_){}
}
function sfx(kind){
 if(!ctx||ctx.state!=='running'||document.hidden||prefs.effectsVolume===0)return;
 const now=ctx.currentTime;if(kind==='click'&&now-lastClick<.045)return;if(kind==='click')lastClick=now;
 const notes={click:[660,990],upgrade:[392,523,784],planet:[220,330,440,660],evolve:[262,392,523,784,1047],build:[196,294,392],ready:[523,784],pulse:[131,262,392,784],sync:[660,880],retry:[262,220]}[kind]||[440];
 notes.forEach((f,i)=>tone(f,now+i*(kind==='click'?.022:.08),kind==='click'?.10:.42,kind==='click'?.07:.09,effects,kind==='build'?'triangle':'sine'));
}
function updateUI(){const b=document.getElementById('musicToggle');b.textContent=prefs.musicConsent?'Wyłącz muzykę':'Włącz muzykę — zgadzam się';b.setAttribute('aria-pressed',String(prefs.musicConsent));for(const [id,key] of [['musicVolume','musicVolume'],['effectsVolume','effectsVolume']]){document.getElementById(id).value=Math.round(prefs[key]*100);document.getElementById(id+'Value').textContent=Math.round(prefs[key]*100)+'%'}}
function init(){
 updateUI();document.getElementById('musicToggle').onclick=async()=>{prefs.musicConsent=!prefs.musicConsent;store();if(prefs.musicConsent)await gesture();else stopMusic();updateUI()};
 for(const key of ['musicVolume','effectsVolume'])document.getElementById(key).oninput=e=>{prefs[key]=Math.max(0,Math.min(1,Number(e.target.value)/100));store();if(ctx){const gain=key==='musicVolume'?music:effects;gain.gain.setTargetAtTime(prefs[key],ctx.currentTime,.08);if(key==='musicVolume'){if(!prefs[key])stopMusic();else if(prefs.musicConsent&&timer===null)gesture()}}updateUI()};
 document.addEventListener('visibilitychange',()=>{if(document.hidden){stopMusic();if(ctx)ctx.suspend().catch(()=>{})}else if(started)gesture()});window.addEventListener('pagehide',()=>{stopMusic();if(ctx)ctx.suspend().catch(()=>{})});
}
window.NeonAudio={init,gesture,sfx,getPreferences:()=>({...prefs})};
})();
