/* MiracuVerse music library: standalone hash-routed playlists and custom HTML5 audio player. */
(()=>{'use strict';
const app=document.getElementById('app');
let catalog=[],selected=null,audio=new Audio(),current=null,active=false,shuffle=false,repeat=false;
audio.preload='metadata';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const format=n=>Number.isFinite(n)?Math.floor(n/60)+':'+String(Math.floor(n%60)).padStart(2,'0'):'--:--';
const url=s=>{try{const u=new URL(s,location.href);return ['https:','http:'].includes(u.protocol)?u.href:''}catch{return ''}};
const cover=(p,cls)=>p.cover&&url(p.cover)?'<img class="'+cls+'" src="'+esc(url(p.cover))+'" alt="'+esc(p.title)+' cover" loading="lazy">':'<span class="mv-cover-placeholder">♫</span>';
const find=()=>catalog.find(p=>p.id===selected);
const allSongs=()=>find()?.songs||[];
const route=()=>decodeURIComponent(location.hash.slice(1).split('?')[0]||'/');
const isMusic=()=>route()==='/music'||route().startsWith('/music/');
async function load(){
 try{const r=await fetch('./music-library.json?ts='+Math.floor(Date.now()/60000),{cache:'no-store'});if(!r.ok)throw Error('No music catalog');const j=await r.json();catalog=(Array.isArray(j.playlists)?j.playlists:[]).filter(p=>p&&typeof p.id==='string'&&Array.isArray(p.songs));}
 catch(e){console.warn('Music catalog could not be loaded',e);catalog=[]}
 if(isMusic())render();
}
function stop(){audio.pause();audio.removeAttribute('src');audio.load();current=null;active=false;document.querySelector('.mv-player')?.remove();refreshRows()}
function refreshRows(){document.querySelectorAll('[data-mv-play]').forEach(b=>{const playing=current&&b.dataset.mvPlay===current.id&&active;b.textContent=playing?'❚❚':'▶';b.setAttribute('aria-label',playing?'Pause':'Play')})}
function play(song){if(!song)return;const src=url(song.src||'');if(!src){const n=document.getElementById('mv-notice');if(n)n.textContent='Add an MP3 URL for this track in music-library.json first.';return}
 if(current?.id===song.id){if(audio.paused)audio.play().catch(onError);else audio.pause();return}
 current=song;audio.src=src;audio.playbackRate=Number(document.getElementById('mv-speed')?.value||1);audio.play().catch(onError);player();refreshRows()}
function onError(){const n=document.getElementById('mv-notice');if(n)n.textContent='This audio URL cannot be played. Check the link and permissions.'}
function next(step=1){const list=allSongs().filter(s=>url(s.src||''));if(!list.length){stop();return}let idx=list.findIndex(s=>s.id===current?.id);if(shuffle&&list.length>1){let pick=Math.floor(Math.random()*(list.length-1));idx=pick>=idx?pick+1:pick-step}else idx+=step;if(idx>=list.length){if(repeat)idx=0;else{stop();return}}if(idx<0)idx=list.length-1;play(list[idx])}
function player(){document.querySelector('.mv-player')?.remove();const host=document.getElementById('mv-player-host');if(!host||!current)return;host.innerHTML='<section class="mv-player" aria-label="Music player"><div class="mv-player-heading"><div class="mv-now"><span class="mv-now-icon">♫</span><div><strong id="mv-now-title">'+esc(current.title)+'</strong><small>'+esc(current.artist||'')+'</small></div></div><button class="mv-close" id="mv-close" aria-label="Close player">✕</button></div><div class="mv-transport"><button id="mv-shuffle" title="Shuffle" aria-label="Shuffle">⇄</button><button id="mv-prev" aria-label="Previous">⏮</button><button id="mv-toggle" class="mv-play-main" aria-label="Pause">❚❚</button><button id="mv-next" aria-label="Next">⏭</button><button id="mv-repeat" title="Repeat" aria-label="Repeat">↻</button></div><div class="mv-progress"><span id="mv-time">0:00</span><input id="mv-seek" type="range" min="0" max="1000" value="0" aria-label="Seek through track"><span id="mv-total">--:--</span></div><div class="mv-player-options"><label>Speed <select id="mv-speed"><option value="0.5">0.5×</option><option value="0.75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option><option value="2">2×</option></select></label><label>Volume <input id="mv-volume" type="range" min="0" max="100" value="'+Math.round(audio.volume*100)+'" aria-label="Volume"></label></div></section>';
 document.getElementById('mv-close').onclick=stop;
 document.getElementById('mv-toggle').onclick=()=>{if(audio.paused)audio.play().catch(onError);else audio.pause()};
 document.getElementById('mv-prev').onclick=()=>next(-1);
 document.getElementById('mv-next').onclick=()=>next(1);
 document.getElementById('mv-shuffle').onclick=()=>{shuffle=!shuffle;document.getElementById('mv-shuffle').classList.toggle('mv-on',shuffle)};
 document.getElementById('mv-repeat').onclick=()=>{repeat=!repeat;document.getElementById('mv-repeat').classList.toggle('mv-on',repeat)};
 document.getElementById('mv-seek').oninput=e=>{if(Number.isFinite(audio.duration)&&audio.duration>0)audio.currentTime=audio.duration*Number(e.target.value)/1000};
 document.getElementById('mv-speed').onchange=e=>audio.playbackRate=Number(e.target.value);
 document.getElementById('mv-volume').oninput=e=>audio.volume=Number(e.target.value)/100;
 update();
}
function update(){if(!current)return;const seek=document.getElementById('mv-seek');if(seek){seek.value=audio.duration?Math.round(audio.currentTime/audio.duration*1000):0;document.getElementById('mv-time').textContent=format(audio.currentTime);document.getElementById('mv-total').textContent=format(audio.duration)}const b=document.getElementById('mv-toggle');if(b){b.textContent=audio.paused?'▶':'❚❚';b.setAttribute('aria-label',audio.paused?'Play':'Pause')}refreshRows()}
audio.addEventListener('timeupdate',update);audio.addEventListener('loadedmetadata',update);audio.addEventListener('play',()=>{active=true;update()});audio.addEventListener('pause',()=>{active=false;update()});audio.addEventListener('ended',()=>next());audio.addEventListener('error',onError);
function render(){if(!isMusic())return;const path=route();selected=path.startsWith('/music/')?path.slice(7):null;const p=find();document.title=(p?p.title:'Music')+' | MiracuVerse';
if(!p){app.innerHTML='<div class="page-heading"><div><span class="eyebrow">MUSIC COLLECTION</span><h1>Music <span class="gradient">Library</span></h1><p>Explore playlists, soundtracks and collections.</p></div></div><div class="mv-playlists">'+catalog.map(x=>'<a class="mv-playlist-card" href="#/music/'+encodeURIComponent(x.id)+'"><div class="mv-playlist-art">'+cover(x,'mv-cover')+'</div><h3>'+esc(x.title)+'</h3><p>'+x.songs.length+' tracks</p></a>').join('')+'</div>'+(catalog.length?'':'<div class="empty">Add playlists in music-library.json to get started.</div>');return}
app.innerHTML='<div class="mv-back"><a href="#/music">← Back to music library</a></div><div class="mv-playlist-detail"><div class="mv-playlist-left"><div class="mv-large-art">'+cover(p,'mv-cover')+'</div><h1>'+esc(p.title)+'</h1><p>'+esc(p.description||'')+'</p><span>'+p.songs.length+' tracks</span></div><div class="mv-track-panel"><div class="mv-track-head"><span>TRACK</span><span>DURATION</span></div><div class="mv-track-list">'+p.songs.map((s,i)=>'<div class="mv-track"><button class="mv-track-play" data-mv-play="'+esc(s.id)+'" data-index="'+i+'" aria-label="Play '+esc(s.title)+'">▶</button><div class="mv-track-info"><strong>'+esc(s.title)+'</strong><small>'+esc(s.artist||'')+'</small></div><time>'+esc(s.duration||'--:--')+'</time></div>').join('')+'</div>'+(p.songs.length?'':'<p class="mv-empty">No tracks yet. Add them in music-library.json.</p>')+'<p id="mv-notice" role="status"></p></div></div><div id="mv-player-host"></div>';
app.querySelectorAll('[data-mv-play]').forEach(b=>b.onclick=()=>play(p.songs[Number(b.dataset.index)]));if(current){if(!p.songs.some(s=>s.id===current.id))stop();else player()}refreshRows();
}
window.MV_MUSIC={render,stop};window.addEventListener('hashchange',()=>{if(!isMusic())stop();else render()});load();
})();
