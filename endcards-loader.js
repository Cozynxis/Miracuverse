/* Load verified production order and image index without manual per-episode edits. */
(async()=>{
 const normalize=s=>String(s||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]/g,'');
 try{
   const [orderResponse,imageResponse]=await Promise.all([
     fetch('./episode-order.json?ts='+Math.floor(Date.now()/3600000),{cache:'no-store'}),
     fetch('./endcards.json?ts='+Math.floor(Date.now()/3600000),{cache:'no-store'})
   ]);
   const order=orderResponse.ok?await orderResponse.json():{};
   const images=imageResponse.ok?await imageResponse.json():{};
   const episodes=window.MV_EPISODES||[];
   const original=episodes.map(e=>({...e}));
   const byTitle=new Map(original.map(e=>[e.season+':'+normalize(e.title),e]));
   const aliases={'theevillustrator':'theevilustrator','misteragreste':'mragreste','grendiaper':'grandiaper'};
   const canonical=s=>aliases[normalize(s)]||normalize(s);
   const imageByTitle=new Map();
   for(const e of original){
     const url=images[e.season+'-'+e.episode];
     if(typeof url==='string'&&/^https:\/\/(static|vignette)\.wikia\.nocookie\.net\//i.test(url))
       imageByTitle.set(e.season+':'+canonical(e.title),url);
   }
   if(order&&typeof order==='object'){
     for(const [season,titles] of Object.entries(order)){
       if(!Array.isArray(titles)||!titles.length)continue;
       const number=Number(season);
       const current=episodes.filter(e=>e.season===number);
       if(current.length!==titles.length)continue;
       const lookup=new Map(current.map(e=>[canonical(e.title),e]));
       if(titles.some(t=>!lookup.has(canonical(t))))continue;
       const updated=titles.map((title,i)=>({...lookup.get(canonical(title)),episode:i+1}));
       episodes.splice(0,episodes.length,...episodes.filter(e=>e.season!==number),...updated);
     }
     episodes.sort((a,b)=>a.season-b.season||a.episode-b.episode);
   }
   const overrides={};
   // Images in endcards.json are already keyed by the published episode number.
   // Do not remap twice or filter them through an incorrectly escaped regex.
   for(const [key,url] of Object.entries(images)){
     if(typeof url==='string' && url.startsWith('https://static.wikia.nocookie.net/')){
       overrides[key]=url;
     }
   }
   Object.assign(window.MV_IMAGE_OVERRIDES||{},overrides);
   window.dispatchEvent(new Event('hashchange'));
 }catch(error){console.warn('Episode catalog update unavailable:',error)}
})();