# MiracuVerse Cinema — episode video player

The cinema UI is loaded only on `#/episode/SEASON-EPISODE` pages. It uses the existing episode endcard as the video poster and does **not** change episode data, ordering, images, or endcard loaders.

## Add a licensed video later

Edit `episode-videos.json`. Use the exact episode key from the route, e.g. `1-1` for season 1, episode 1.

```json
{
  "version": 1,
  "episodes": {
    "1-1": {
      "sources": [
        { "label": "1080p", "src": "https://your-domain.example/video-1080.mp4", "type": "video/mp4" },
        { "label": "720p", "src": "https://your-domain.example/video-720.mp4", "type": "video/mp4" }
      ],
      "subtitles": [
        { "label": "English", "srclang": "en", "src": "https://your-domain.example/subtitles-en.vtt" }
      ]
    }
  }
}
```

Use direct HTTPS video file URLs supported by HTML5 video, such as MP4 (H.264/AAC), and WebVTT subtitle URLs. The browser must be allowed to fetch them (CORS may apply). HLS/DASH streaming is not yet supported by this version. Do not use a YouTube watch page or iframe URL as a direct video source.

## Features

- Endcard poster with prominent Watch Episode button
- Accessible overlay cinema with responsive design
- Play/pause, seeking and ±10-second jumps
- Volume, mute, speed (0.5–2×), multiple quality/source choices
- WebVTT subtitles, fullscreen, picture-in-picture, theater mode
- Buffered progress and formatted time
- Keyboard controls: Space/K, J/L, arrow keys, M, F, Escape
- Local playback position saved per episode and restored on next opening
- Clear video-unavailable and loading-error messages
- No auto-play of videos until explicitly requested

Videos are **not** included in the repository. Only upload or link content you are authorized to distribute. The player's feature availability depends on browser support and the video files provided.
