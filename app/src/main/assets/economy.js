/* Pure economy rules shared by the game and regression tests. */
(function(root){
'use strict';
const ids=['luna','mars','titan'];
const technologies=[
 {id:'lattice',name:'Sieć nadprzewodząca',level:1,cost:300000,production:.10,click:0,desc:'+10% produkcji'},
 {id:'resonance',name:'Rezonans rdzenia',level:4,cost:1800000,production:0,click:.50,desc:'+50% energii z dotknięcia'},
 {id:'vacuum',name:'Energia próżni',level:7,cost:10000000,production:.25,click:0,desc:'+25% produkcji'},
 {id:'heart',name:'Serce Tytana',level:10,cost:50000000,production:0,click:1,desc:'+100% energii z dotknięcia'}
];
function colonyLevel(s,id){
 if(!s.planets?.[id])return 0;
 const n=s.colonies?.[id];
 return Number.isInteger(n)?Math.max(1,Math.min(10,n)):1;
}
function normalizeColonies(s){return Object.fromEntries(ids.map(id=>[id,colonyLevel(s,id)]))}
function colonyCost(s,p){const lv=colonyLevel(s,p.id);return lv>=10?null:Math.floor(p.need*.75*Math.pow(1.85,Math.max(0,lv-1)))}
function lunaMining(s){const lv=colonyLevel(s,'luna');return 20*lv*lv}
function marsMultiplier(s){return 1+.08*colonyLevel(s,'mars')}
function techBonus(s,kind){return technologies.reduce((a,t)=>a+(s.technologies?.[t.id]&&colonyLevel(s,'titan')>=t.level?t[kind]:0),0)}
function production(s,defs,research,planets){
 const base=defs.reduce((a,d)=>a+(s.levels[d.id]||0)*d.power,0);
 const researchMultiplier=1+research.reduce((a,r)=>a+(s.research[r.id]?r.mult-1:0),0);
 // Legacy planet flags are counted exactly once; colony benefits are separate.
 const legacyMultiplier=1+planets.reduce((a,p)=>a+(s.planets[p.id]?p.bonus:0),0);
 const multiplier=researchMultiplier*legacyMultiplier*marsMultiplier(s)*(1+techBonus(s,'production'));
 return {base,mining:lunaMining(s),multiplier,total:(base+lunaMining(s))*multiplier,miningTotal:lunaMining(s)*multiplier};
}
function tapEnergy(s,rate){return Math.ceil((1+Math.floor(rate*.05))*(1+.10*colonyLevel(s,'titan'))*(1+techBonus(s,'click')))}
function buildColony(s,p){
 const lv=colonyLevel(s,p.id),cost=colonyCost(s,p);
 if(!lv||cost===null||!Number.isFinite(s.energy)||s.energy<cost)return false;
 s.energy-=cost;s.colonies=normalizeColonies(s);s.colonies[p.id]=lv+1;return true;
}
function unlockPlanet(s,p){if(s.planets[p.id]||s.total<p.need)return false;s.planets[p.id]=true;s.colonies=normalizeColonies(s);return true}
function buyTechnology(s,t){if(!technologies.includes(t)||s.technologies?.[t.id]||colonyLevel(s,'titan')<t.level||s.energy<t.cost)return false;s.energy-=t.cost;s.technologies={...s.technologies,[t.id]:true};return true}
const api={technologies,colonyLevel,normalizeColonies,colonyCost,lunaMining,marsMultiplier,production,tapEnergy,buildColony,unlockPlanet,buyTechnology,techBonus};
if(typeof module==='object'&&module.exports)module.exports=api;else root.NeonEconomy=api;
})(typeof window!=='undefined'?window:globalThis);
