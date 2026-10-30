# MiracuVerse Music Library — handleiding

De website haalt playlists en nummers uit [music-library.json](../music-library.json).

## Eenvoudig toevoegen zonder JSON te schrijven
1. Open [Music Manager](https://cozynxis.github.io/Miracuverse/music-manager.html).
2. Klik **Huidige library ophalen** (de manager doet dit ook automatisch).
3. Klik **+ Nieuwe playlist** of kies de bestaande **Miraculous World: London**.
4. Vul de playlistnaam, beschrijving en coverlink in.
5. Klik **+ Nummer toevoegen** en vul titel, artiest, optionele duur en MP3-pad in.
6. Je kunt nummers met ↑ en ↓ herschikken of verwijderen.
7. Klik **Kopieer JSON**, open **GitHub editor**, vervang de bestaande inhoud en klik **Commit changes**. Of download het JSON-bestand en upload het als vervanging.
8. Wacht op GitHub Pages en open de Music Library opnieuw.

## MP3 uploaden
1. Open [GitHub upload naar music](https://github.com/Cozynxis/Miracuverse/upload/main/music).
2. Upload een MP3 (maximaal 25 MB via de GitHub-webinterface) en commit.
3. Vul bij **MP3-URL of pad** in: `music/jouw-bestand.mp3`.
4. Test de playlist op de site.

Je kunt ook een volledige HTTPS-link naar een MP3 gebruiken. De bron moet rechtstreeks afspeelbaar zijn.

## Covers
Gebruik een afbeelding-URL (HTTPS) of upload de afbeelding naar de repository en vul bijvoorbeeld `music/covers/london.jpg` in.

## Belangrijk
De manager slaat wijzigingen **niet direct** op GitHub op. Publiceren vereist een commit van `music-library.json`. De manager is een lokale editor in de browser, zonder login. Bestanden in een openbare GitHub-repository zijn publiek. Upload alleen audio waarvoor je toestemming hebt.
