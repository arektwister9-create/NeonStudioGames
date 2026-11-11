/* Turn-based core expeditions: no real-time pressure and no energy gates. */
(function(root){
'use strict';
const MAX=30,worlds=[
 {name:'Pas rozbitków',color:'#e3ad73',titles:['Pierwszy przesmyk','Pole wraków','Zaszyfrowany sygnał','Kryształowy rój','Strażnik pasa']},
 {name:'Lodowa granica',color:'#79ecff',titles:['Lodowe odłamki','Błękitna stacja','Burza sygnałów','Pęknięta orbita','Strażnik lodu']},
 {name:'Mgławica burz',color:'#bd8bff',titles:['Fioletowe echo','Jonowa zapora','Ukryty nadajnik','Węzły burzy','Strażnik mgławicy']},
 {name:'Kuźnia gwiazd',color:'#ff9970',titles:['Żar korony','Odłamki słońca','Słoneczny przekaźnik','Reaktor olbrzyma','Strażnik kuźni']},
 {name:'Cicha otchłań',color:'#7fafff',titles:['Ciemna materia','Zaginiona flota','Głęboki nasłuch','Granica ciszy','Strażnik otchłani']},
 {name:'Serce galaktyki',color:'#ffdc79',titles:['Złote odłamki','Ostatnia stacja','Sygnał źródła','Trzy pieczęcie','Architekt rdzenia']}
];
const tools=[{name:'Impuls',verb:'Rozbij',glyph:'ϟ'},{name:'Skaner',verb:'Zeskanuj',glyph:'◎'},{name:'Osłona',verb:'Ustabilizuj',glyph:'⬡'}];
const buildings=[{id:'dock',name:'Dok dronów',desc:'Odblokowuje atak obszarowy; każdy poziom wzmacnia drony.'},{id:'lab',name:'Laboratorium',desc:'Co 2 poziomy: +1 obrażenie poprawnego narzędzia.'},{id:'shield',name:'Generator osłon',desc:'Każdy poziom: +2 osłony podczas ekspedycji.'}];
const int=(n,lo,hi)=>Number.isInteger(n)?Math.max(lo,Math.min(hi,n)):lo;
function info(level){level=int(level,1,MAX);const sector=Math.floor((level-1)/5);return {level,sector,boss:level%5===0,...worlds[sector],title:worlds[sector].titles[(level-1)%5]}}
function unlockedTools(cleared){return cleared>=7?3:cleared>=2?2:1}
function phaseTargets(level,phase,cleared){const m=info(level),count=m.boss?1:3,toolCount=unlockedTools(cleared);return Array.from({length:count},(_,i)=>({max:m.boss?6+m.sector*2+phase:2+Math.floor(m.sector/2)+(i+phase)%2,tool:(level+phase+i)%toolCount}))}
function normalized(x){
 x=x&&typeof x==='object'?x:{};
 const out={cleared:int(x.cleared,0,MAX),materials:int(x.materials,0,1000000000),modules:{},tool:int(x.tool,0,2),active:null};
 for(const b of buildings)out.modules[b.id]=int(x.modules?.[b.id],0,6);
 out.tool=Math.min(out.tool,unlockedTools(out.cleared)-1);
 if(x.active&&Number.isInteger(x.active.level)&&x.active.level>=1&&x.active.level<=Math.min(MAX,out.cleared+1)){
  const a=x.active,m=info(a.level),phase=int(a.phase,0,m.boss?2:1),targets=phaseTargets(a.level,phase,out.cleared),health=int(a.health,0,6+out.modules.shield*2);
  if(health>0)out.active={level:a.level,phase,health,hp:targets.map((t,i)=>Number.isInteger(a.hp?.[i])?int(a.hp[i],0,t.max):t.max),support:int(a.support,0,3),rotation:int(a.rotation,0,1000000),repairUsed:a.repairUsed===true};
 }
 if(out.active&&out.active.hp.every(h=>h===0))out.active.hp=phaseTargets(out.active.level,out.active.phase,out.cleared).map(t=>t.max);
 return out;
}
function state(s){s.expedition=normalized(s.expedition);return s.expedition}
function buildCost(s,id){const x=normalized(s.expedition);return x.modules[id]===undefined||x.modules[id]>=6?null:2*(x.modules[id]+1)}
function upgrade(s,id){const x=state(s),cost=buildCost(s,id);if(cost===null||x.materials<cost||x.active)return false;x.materials-=cost;x.modules[id]++;return true}
function requiredGrade(level){return Math.floor((level-1)/5)}
function canStart(s,level){const x=normalized(s.expedition);return Number.isInteger(level)&&level>=1&&level<=Math.min(MAX,x.cleared+1)&&!x.active&&Math.max(...Object.values(x.modules))>=requiredGrade(level)}
function start(s,level){const x=state(s);if(!canStart(s,level))return false;const targets=phaseTargets(level,0,x.cleared);x.active={level,phase:0,health:6+x.modules.shield*2,hp:targets.map(t=>t.max),support:0,rotation:0,repairUsed:false};return true}
function choose(s,tool){const x=state(s);if(!Number.isInteger(tool)||tool<0||tool>=unlockedTools(x.cleared))return false;x.tool=tool;return true}
function targetTool(s,index){const x=normalized(s.expedition),a=x.active;if(!a)return null;const t=phaseTargets(a.level,a.phase,x.cleared)[index];return t?(t.tool+(info(a.level).boss?a.rotation:0))%unlockedTools(x.cleared):null}
function advance(s,x){const a=x.active,m=info(a.level);if(a.hp.some(h=>h>0))return {kind:'hit'};
 if(a.phase<(m.boss?2:1)){a.phase++;a.rotation=0;a.hp=phaseTargets(a.level,a.phase,x.cleared).map(t=>t.max);return {kind:'wave'}}
 const first=a.level>x.cleared,reward=first?2+m.sector:1+Math.floor(m.sector/2),energy=first?100*a.level*(m.sector+1):0;x.materials+=reward;if(first)x.cleared=a.level;s.energy+=energy;s.total+=energy;x.active=null;return {kind:'victory',first,reward,energy,level:a.level};
}
function strike(s,index){const x=state(s),a=x.active;if(!a||!Number.isInteger(index)||index<0||index>=a.hp.length||a.hp[index]<=0)return {kind:'inactive'};
 if(x.tool!==targetTool(s,index)){a.health-=2;if(a.health<=0){x.active=null;return {kind:'defeat'}}return {kind:'blocked'}}
 a.hp[index]=Math.max(0,a.hp[index]-(1+Math.floor(x.modules.lab/2)));a.support=Math.min(3,a.support+1);if(info(a.level).boss)a.rotation++;return advance(s,x);
}
function support(s){const x=state(s),a=x.active;if(!a||!x.modules.dock||a.support<3)return {kind:'inactive'};a.support=0;a.hp=a.hp.map(h=>Math.max(0,h-(1+x.modules.dock)));return advance(s,x)}
function repairCost(s){const a=normalized(s.expedition).active;return a?100*(info(a.level).sector+1)**2:null}
function repair(s){const x=state(s),a=x.active,cost=repairCost(s);if(!a||a.repairUsed||a.health>=6+x.modules.shield*2||s.energy<cost)return false;s.energy-=cost;a.health=Math.min(6+x.modules.shield*2,a.health+4);a.repairUsed=true;return true}
function retreat(s){const x=state(s);if(!x.active)return false;x.active=null;return true}
const api={MAX,worlds,tools,buildings,info,unlockedTools,phaseTargets,normalized,state,buildCost,upgrade,requiredGrade,canStart,start,choose,targetTool,strike,support,repairCost,repair,retreat};
if(typeof module==='object'&&module.exports)module.exports=api;else root.NeonExpedition=api;
})(typeof window!=='undefined'?window:globalThis);
