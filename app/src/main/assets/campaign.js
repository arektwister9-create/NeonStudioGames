/* Core awakening campaign. Pure rules: no timers, DOM, audio, or storage. */
(function(root){
'use strict';
const chapters=[
 {title:'Pierwszy sygnał',story:'W rdzeniu ukryto mapę. Zbuduj odbiornik i wyślij pierwszy puls.',reward:250,pattern:[0,2,1],pulses:1,goals:[['drone',3]]},
 {title:'Latarnia Luna-9',story:'Kopalnie odbierają echo z głębi kosmosu. Zmień Lunę w pierwszą latarnię.',reward:2500,pattern:[1,0,2,1],pulses:3,goals:[['luna',2]]},
 {title:'Przekaźnik Marsa',story:'Przemysł Marsa zasili nadajnik. Połącz kolonie w jedną sieć.',reward:15000,pattern:[2,1,0,2],pulses:5,goals:[['mars',3],['overclock',1]]},
 {title:'Echo Tytana',story:'Tytan odpowiada. Jego technologie odsłaniają współrzędne uśpionej bramy.',reward:75000,pattern:[0,1,2,0,2],pulses:8,goals:[['titan',2],['lattice',1]]},
 {title:'Stabilizacja bramy',story:'Trzy latarnie muszą pracować razem. Zsynchronizuj je z rezonansem rdzenia.',reward:250000,pattern:[2,0,1,2,1],pulses:12,goals:[['allColonies',5],['resonance',1]]},
 {title:'Po drugiej stronie',story:'Brama jest gotowa. Obudź serce Tytana i wyślij ostatnią sekwencję.',reward:1000000,pattern:[1,2,0,2,1,0],pulses:18,goals:[['allColonies',7],['titan',10],['heart',1]]}
];
const names={drone:'Drony zbierające',luna:'Kolonia Luna-9',mars:'Kolonia Mars Prime',titan:'Kolonia Tytana',overclock:'Badanie: Nadprzewodnictwo',lattice:'Technologia: Sieć nadprzewodząca',resonance:'Technologia: Rezonans rdzenia',heart:'Technologia: Serce Tytana',allColonies:'Każda z trzech kolonii'};
const integer=(n,max=Number.MAX_SAFE_INTEGER)=>Number.isSafeInteger(n)?Math.max(0,Math.min(max,n)):0;
function normalized(x){
 x=x&&typeof x==='object'?x:{};
 const chapter=integer(x.chapter,chapters.length),pattern=chapters[chapter]?.pattern;
 return {chapter,charge:integer(x.charge,12),pulses:integer(x.pulses),syncActive:!!pattern&&x.syncActive===true,syncIndex:pattern?integer(x.syncIndex,pattern.length-1):0};
}
function state(s){s.coreCampaign=normalized(s.coreCampaign);return s.coreCampaign}
function capacity(s){return Math.max(8,12-Math.floor(normalized(s.coreCampaign).chapter/2))}
function goalValue(s,id,economy){if(id==='drone')return s.levels.drone||0;if(id==='allColonies')return Math.min(...['luna','mars','titan'].map(p=>economy.colonyLevel(s,p)));if(['luna','mars','titan'].includes(id))return economy.colonyLevel(s,id);return s.research?.[id]||s.technologies?.[id]?1:0}
function progress(s,economy){
 const c=normalized(s.coreCampaign),chapter=chapters[c.chapter];if(!chapter)return [];
 return [{id:'pulses',name:'Wyzwolone pulsy',value:c.pulses,need:chapter.pulses},...chapter.goals.map(([id,need])=>({id,name:names[id],value:goalValue(s,id,economy),need}))];
}
function ready(s,economy){const goals=progress(s,economy);return goals.length>0&&goals.every(g=>g.value>=g.need)}
function charge(s){const c=state(s),before=c.charge;c.charge=Math.min(capacity(s),c.charge+1);return before<capacity(s)&&c.charge===capacity(s)}
function pulseReward(s,rate,tap){const c=normalized(s.coreCampaign);return Math.ceil(Math.max(25,rate*15+tap*8)*(1+c.chapter*.15))}
function release(s,rate,tap){const c=state(s);if(c.charge<capacity(s))return 0;const reward=pulseReward(s,rate,tap);c.charge=0;c.pulses++;s.energy+=reward;s.total+=reward;return reward}
function begin(s,economy){const c=state(s);if(c.syncActive||!ready(s,economy))return false;c.syncActive=true;c.syncIndex=0;return true}
function select(s,node,economy){
 const c=state(s),chapter=chapters[c.chapter];if(!chapter||!c.syncActive||!ready(s,economy)||![0,1,2].includes(node))return 'inactive';
 if(node!==chapter.pattern[c.syncIndex]){c.syncIndex=0;return 'retry'}
 c.syncIndex++;
 if(c.syncIndex<chapter.pattern.length)return 'step';
 c.chapter++;c.syncActive=false;c.syncIndex=0;c.charge=Math.min(c.charge,capacity(s));s.energy+=chapter.reward;s.total+=chapter.reward;return 'complete';
}
const api={chapters,normalized,state,capacity,progress,ready,charge,pulseReward,release,begin,select};
if(typeof module==='object'&&module.exports)module.exports=api;else root.NeonCampaign=api;
})(typeof window!=='undefined'?window:globalThis);
