# MiracuVerse Characters & Kwamis API

This is a static JSON API that works on GitHub Pages without keys or a server.

- Public endpoint: https://cozynxis.github.io/Miracuverse/api/characters.json
- Editor: https://github.com/Cozynxis/Miracuverse/edit/main/api/characters.json
- Website: https://cozynxis.github.io/Miracuverse/#/about

## Add a picture
Find the existing entry by exact `name` and fill in its `image` field with a public, direct HTTPS image URL:

```json
{
  "name": "Tikki",
  "image": "https://example.com/tikki.png",
  "description": "Kwami of Creation.",
  "power": "Creation",
  "miraculous": "Ladybug",
  "wiki": "Tikki"
}
```

`image` can be blank; a styled initial placeholder is shown until you add an image. You can also set `description`, `power`, `miraculous`, `subtitle`, `group`, `concept`, and `wiki` (the Miraculous Wiki page title).

**Do not remove the `characters` or `kwamis` arrays.** Keep JSON commas and quotes valid.

The site retains the complete original list from `catalog.js` and merges these overrides by exact name. Adding a new name in this file does not automatically create a new base entry; add new names to `catalog.js` first.

The catalog loads independently from episodes. If this JSON fails to load, the original character and kwami data still render. Episode files, endcards and music are not modified.

Use images you have permission to publish or embed. External image hosts can block hotlinking; use your own hosted files for the most reliable results.
