/* Local browser compatibility only. No network requests or telemetry. */
(function(){
 'use strict';
 function define(object,key,value){Object.defineProperty(object,key,{configurable:true,writable:true,value:value})}
 if(!Object.assign)define(Object,'assign',function(target){if(target==null)throw new TypeError('Invalid target');var out=Object(target);for(var i=1;i<arguments.length;i++){var source=arguments[i];if(source!=null)Object.keys(Object(source)).forEach(function(key){out[key]=source[key]})}return out});
 if(!Object.values)define(Object,'values',function(object){return Object.keys(object).map(function(key){return object[key]})});
 if(!Object.entries)define(Object,'entries',function(object){return Object.keys(object).map(function(key){return[key,object[key]]})});
 if(!Object.fromEntries)define(Object,'fromEntries',function(entries){var out={};Array.from(entries).forEach(function(entry){Object.defineProperty(out,entry[0],{value:entry[1],enumerable:true,writable:true,configurable:true})});return out});
 if(!Array.from)define(Array,'from',function(list,mapFn){var array=Array.prototype.slice.call(list);return mapFn?array.map(mapFn):array});
 if(!Array.prototype.includes)define(Array.prototype,'includes',function(value,from){var length=this.length>>>0,start=Number(from)||0;if(start<0)start=Math.max(0,length+start);for(var i=start;i<length;i++)if(this[i]===value||(this[i]!==this[i]&&value!==value))return true;return false});
 if(typeof NodeList!=='undefined'&&!NodeList.prototype.forEach)define(NodeList.prototype,'forEach',Array.prototype.forEach);
 if(typeof Element!=='undefined'){
  if(!Element.prototype.append)define(Element.prototype,'append',function(){for(var i=0;i<arguments.length;i++)this.appendChild(arguments[i] instanceof Node?arguments[i]:document.createTextNode(String(arguments[i])))});
  if(!Element.prototype.replaceChildren)define(Element.prototype,'replaceChildren',function(){while(this.firstChild)this.removeChild(this.firstChild);this.append.apply(this,arguments)});
  if(!Element.prototype.remove)define(Element.prototype,'remove',function(){if(this.parentNode)this.parentNode.removeChild(this)});
  if(!Element.prototype.matches)define(Element.prototype,'matches',Element.prototype.webkitMatchesSelector);
 }
 if(typeof Blob!=='undefined'&&!Blob.prototype.text)define(Blob.prototype,'text',function(){var blob=this;return new Promise(function(resolve,reject){var reader=new FileReader();reader.onload=function(){resolve(reader.result)};reader.onerror=function(){reject(reader.error)};reader.readAsText(blob)})});
 if(typeof window!=='undefined'&&typeof document!=='undefined'){
  window.NeonUnsupportedWebView=!(window.CSS&&window.CSS.supports&&window.CSS.supports('--neon-test','0'));
  if(window.NeonUnsupportedWebView){var notice=document.getElementById('compatNotice');if(notice)notice.style.display='block'}
 }
})();
