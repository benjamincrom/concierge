(function(){window.pigeon=window.pigeon||{};;(function(){"function"!=typeof pigeon.claimTag&&(pigeon.claimTag=function(d){for(var c=document.getElementsByTagName("script"),b=0;b<c.length;b++){var a=c[b];if(-1<a.src.indexOf(d)&&!a.sayUsed)return a.sayUsed=!0,a}})})();;(function(){"undefined"==typeof pigeon.createIframe&&(pigeon.createIframe=function(d,b){var a=document.createElement("iframe");b&&(a.src=b);a.setAttribute("frameBorder","0");a.setAttribute("marginWidth","0");a.setAttribute("marginHeight","0");a.setAttribute("allowTransparency","true");a.setAttribute("scrolling","no");a.setAttribute("vspace","0");a.setAttribute("hspace","0");var c=d.split("x");a.style.padding="0px";a.style.marginTop="0px";a.style.marginLeft="auto";a.style.marginRight=
"auto";a.style.width=c[0]+"px";a.style.height=c[1]+"px";return a})})();
;(function(){function c(){this.isDebug=/debug=1/.test(window.location.toString());var b=function(a,b){"undefined"!=typeof console&&console.log(a+" "+(new Date).toString()+" "+b)};this.error=function(a){b("ERROR",a)};this.debug=function(a){this.isDebug&&b("DEBUG",a)}}"undefined"==typeof pigeon.log&&(pigeon.log=new c)})();
;;function ReadyHandler(){var b=!1,c=[];"complete"==document.readyState&&(b=!0);var a=function(){for(b=!0;0<c.length;)c.shift()()};document.addEventListener?(document.addEventListener("DOMContentLoaded",a,!1),window.addEventListener("load",a,!1)):document.attachEvent&&(document.attachEvent("onreadystatechange",a,!1),window.attachEvent("onload",a));this.ready=function(a){b?a():c.push(a)}}"undefined"==typeof pigeon.ready&&function(){var b=new ReadyHandler;pigeon.ready=function(c){b.ready(c)}}();
;(function(){"undefined"==typeof pigeon.topWindow&&(pigeon.testWindow=function(a){try{var b=a.document.body,c=b.insertBefore(a.document.createComment("accessibile"),b.firstChild);b.removeChild(c);return!0}catch(d){return pigeon.log.debug("Exception testing window access: "+d),!1}},pigeon.topWindow=function(){var a;try{a=top,pigeon.log.debug("No exception on top.document")}catch(b){}"undefined"==typeof a&&(pigeon.log.debug("No access to top.document"),a=window);a=pigeon.findTopWindow(a);
if(!pigeon.testWindow(a))return pigeon.log.debug("No write access to window, using current window: "+window.location),window;pigeon.log.debug("Write access to window granted");return a},pigeon.findTopWindow=function(a){try{var b=a.document;if("FRAMESET"==b.body.nodeName){for(var c=window;c.parent!==c.parent.parent;c=c.parent);for(var d=b.body.getElementsByTagName("frame"),b=0;b<d.length;b++)if(c===d[b].contentWindow)return c}}catch(e){}return a})})();
;;(function(){"undefined"==typeof pigeon.promoteDomain&&(pigeon.promoteDomain=function(){for(var a=document.domain.split(".");2<a.length;){a.shift();try{if(document.domain=a.join("."),pigeon.testWindow(top))return!0}catch(b){}}return!1})})();
;
"undefined"==typeof pigeon.breakout&&(pigeon.breakout=function(a,b,d,e){pigeon.ready(function(){var c=pigeon.claimTag(b),f;if(pigeon.testWindow(top))f=top;else{if("undefined"!=typeof e&&""!=e){pigeon.log.debug("Using iframe buster: "+e);pigeon.iframeBuster(a,b,d,e,c);return}pigeon.promoteDomain()&&pigeon.testWindow(top)?f=top:(pigeon.log.debug("Failed to access top document"),f=window)}pigeon.log.debug("Reloading script with new referrer");var g=document.createElement("script");g.setAttribute("type",
"text/javascript");g.setAttribute("src",pigeon.buildAdUrl(c,a,{bo:0,ref:escape(f.location)}));c.parentNode.insertBefore(g,c)})},pigeon.iframeBuster=function(a,b,d,e,c){if(/;bo=/.test(c.src))pigeon.log.error("Multiple attempts to break out of iframe");else{d=pigeon.createIframe(d,e);b=b+"_"+a;var f=pigeon.buildAdUrl(c,a,{bo:1});d.src=e+"?rid="+a+"&tagurl="+escape(f)+"&tagid="+b;c.parentNode.insertBefore(d,c)}},pigeon.buildAdUrl=function(a,b,d){a=a.src;-1==a.indexOf(";rid=")&&(a+=";rid="+b);if("undefined"!=
typeof d)for(var e in d){b=escape(e);var c=RegExp(";"+b+"=[^;]*");c.test(a)?a.replace(c,";"+b+"="+escape(d[e])):a+=";"+b+"="+escape(d[e])}return a});
;;var a="516c5b11de010d8c88ce5ad60a1191b6",b="ai017c36e0f525970b017d4110404b970c",c="300x600",d="";pigeon.ready(function(){pigeon.breakout(a,b,c,d)})})();
