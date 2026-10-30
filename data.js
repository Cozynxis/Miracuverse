window.MV_EPISODES=[
...["Stormy Weather","The Bubbler","The Pharaoh","Lady WiFi","Timebreaker","Mr. Pigeon","The Evilustrator","Rogercop","Copy Cat","Dark Cupid","Horrificator","Darkblade","The Mime","Kung Food","The Gamer","Animan","Antibug","Puppeteer","Reflekta","Pixelator","Guitar Villain","Princess Fragrance","Simon Says","Volpina","The Origins - Part 1","The Origins - Part 2"].map((title,i)=>({season:1,episode:i+1,title})),
...["The Collector","Despair Bear","Prime Queen","Befana","Riposte","Robostus","Gigantitan","Dark Owl","Glaciator","Sapotis","Gorizilla","Captain Hardrock","Zombizou","Syren","Frightningale","Troublemaker","Reverser","Anansi","Sandboy","Style Queen","Queen Wasp","Malediktator","Frozer","Catalyst","Mayura","A Christmas Special"].map((title,i)=>({season:2,episode:i+1,title})),
...["Chameleon","Animaestro","Bakerix","Backwarder","Reflekdoll","Weredad","Silencer","Onichan","Miraculer","Oblivio","Desperada","Chris Master","Startrain","Kwami Buster","Feast","Gamer 2.0","Stormy Weather 2","Ikari Gozen","Timetagger","Party Crasher","The Puppeteer 2","Cat Blanc","Felix","Ladybug","Heart Hunter","Miracle Queen"].map((title,i)=>({season:3,episode:i+1,title})),
...["Truth","Lies","Gang of Secrets","Mr Pigeon 72","Psycomedian","Furious Fu","Sole Crusher","Queen Banana","Gabriel Agreste","Mega Leech","Guiltrip","Crocoduel","Optigami","Sentibubbler","Glaciator 2","Hack-San","Rocketear","Wishmaker","Simpleman","Qilin","Dearest Family","Ephemeral","Kuro Neko","Penalteam","Risk","Strike Back"].map((title,i)=>({season:4,episode:i+1,title})),
...["Evolution","Multiplication","Destruction","Jubilation","Illusion","Determination","Passion","Reunion","Elation","Transmission","Deflagration","Perfection","Migration","Derision","Intuition","Protection","Adoration","Emotion","Pretension","Revelation","Confrontation","Collusion","Revolution","Representation","Conformation","Re-Creation","Action"].map((title,i)=>({season:5,episode:i+1,title})),
...["Climatiqueen","The Illustrhater","Sublimation","Daddycop","Werepapas","Sleeping Syren","El Toro De Piedra","Vampigami","Mr. Agreste","The Dark Castle","Revelator","Wreckless Driver","Yaksi Gozen","Grandiaper","The Ruler","Noe","A Fairy Good Night","The Dirtifiers","Riginarazione","Heartfixer","The Chained Titans","Lady Chaos","Sadnansi","Queen Of The Dreadzone","Secret Protocol","Nemesis"].map((title,i)=>({season:6,episode:i+1,title})),
...["New York: United Heroez","Shanghai: The Legend of Lady Dragon","Awakening - The Movie","Paris: Shadybug and Claw Noir","London: At the Edge of Time","Tokyo: Stellar Force"].map((title,i)=>({season:0,episode:i+1,title}))
];
/* Miraculous episode gallery metadata: URLs link to source galleries, not copied images. */
window.MV_EPISODE_GALLERIES={
  "1-25":"Ladybug & Cat Noir (Origins - Part 1)",
  "1-26":"Stoneheart (Origins - Part 2)",
  "2-26":"Santa Claws",
  "3-13":"Christmaster",
  "3-15":"Kwamibuster",
  "3-18":"Oni-Chan",
  "3-23":"Félix",
  "4-26":"Strikeback (Shadow Moth's Final Attack - Part 2)",
  "5-26":"Re-creation (The Final Day - Part 2)"
};
window.MV_GALLERY_PAGE=function(e){
  const key=e.season+"-"+e.episode;
  const title=window.MV_EPISODE_GALLERIES[key]||e.title;
  return "https://miraculousladybug.fandom.com/wiki/"+encodeURIComponent(title.replace(/ /g,"_"))+"/Gallery";
};
window.MV_IMAGE_OVERRIDES={}; // key: '1-1', value: approved image URL
window.MV_EPISODE_IMAGE=function(e){return window.MV_IMAGE_OVERRIDES[e.season+"-"+e.episode]||e.image||"";};
