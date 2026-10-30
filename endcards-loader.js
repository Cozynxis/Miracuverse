/* Endcard loader: automatic catalog + manual overrides. Keep each source independent. */
(async()=>{
  const validUrl=value=>{
    if(typeof value!=='string'||!value.trim())return false;
    try{const parsed=new URL(value.trim());return parsed.protocol==='https:'||parsed.protocol==='http:'}
    catch{return false}
  };
  const read=async path=>{
    try{
      const response=await fetch(path+'?v='+Date.now(),{cache:'no-store'});
      if(!response.ok)throw new Error(path+': '+response.status);
      const result=await response.json();
      return result&&typeof result==='object'?result:{};
    }catch(error){console.warn('MiracuVerse endcards:',error);return {}}
  };
  const [images,manual]=await Promise.all([read('./endcards.json'),read('./manual-endcards.json')]);
  const overrides=window.MV_IMAGE_OVERRIDES||(window.MV_IMAGE_OVERRIDES={});
  let count=0;
  for(const source of [images,manual]){
    for(const [key,value] of Object.entries(source)){
      const parts=key.split('-');
      if(parts.length!==2||parts.some(part=>part===''||!Number.isInteger(Number(part))))continue;
      if(!validUrl(value))continue;
      overrides[key]=value.trim();
      count++;
    }
  }
  console.info('MiracuVerse: loaded '+count+' endcard entries (manual images override automatic images).');
  if(typeof window.MV_EPISODE_IMAGE!=='function'){
    window.MV_EPISODE_IMAGE=e=>overrides[e.season+'-'+e.episode]||e.image||'';
  }
  window.dispatchEvent(new Event('hashchange'));
})();
