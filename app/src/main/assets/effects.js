(()=>{'use strict';
let active=0,last=0;
const reduced=()=>window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function core(add){
 const layer=document.getElementById('coreEffects'),now=performance.now();
 // Maximum eight groups / 56 short-lived nodes; rapid taps still earn full energy.
 if(reduced()||active>=8||now-last<45)return;last=now;active++;
 const group=document.createElement('div');group.className='core-burst';group.setAttribute('aria-hidden','true');
 for(const cls of ['energy-flash','energy-wave']){const e=document.createElement('i');e.className=cls;group.append(e)}
 for(let i=0;i<4;i++){const e=document.createElement('i');e.className='energy-spark';const a=i*Math.PI/2+.4;e.style.setProperty('--dx',Math.cos(a)*96+'px');e.style.setProperty('--dy',Math.sin(a)*96+'px');group.append(e)}
 const value=document.createElement('b');value.className='energy-value';value.textContent='+'+add.toLocaleString('pl-PL');group.append(value);layer.append(group);
 setTimeout(()=>{group.remove();active--},720);
}
function colony(id){if(reduced())return;const scene=document.querySelector('[data-planet="'+id+'"] .planet-scene');if(!scene)return;scene.classList.add('colony-unlock');setTimeout(()=>scene.classList.remove('colony-unlock'),850)}
window.NeonEffects={core,colony};
})();
