# assets

Shared images for the repository and its social cards. (The docs site has its own assets
under `docs/assets/`.)

## `social-preview.png`

The GitHub social preview — the thumbnail shown when this repo is shared on LinkedIn, X,
Slack, or in a newsletter. **1280×640 CSS pixels rendered at 2× (2560×1280), ~504 KB**, inside
GitHub's 1 MB limit.

Uploading it is a web-UI step with no API equivalent:
**Settings → General → Social preview → Edit → Upload an image.**

### Regenerating it

`social-preview.html` is the source. It uses the same brand tokens and typefaces as the docs
site (`docs/assets/css/style.css` — Bitter for the headline, Inter for everything else), so
edit the HTML rather than the PNG, then re-render:

```bash
cd assets
python3 -m http.server 8791 &                    # a local server; file:// won't load webfonts
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 --window-size=1280,640 \
  --screenshot=social-preview.png \
  "http://localhost:8791/social-preview.html"
kill %1
```

Check the result at a small size before shipping it — in most feeds this renders around 600 px
wide, so the headline has to carry the card on its own. Re-upload in Settings after any change;
GitHub does not pick up the file from the repository automatically.

## `demo-contextos.gif` — not yet recorded

Reserved for a short screen recording of a ContextOS build, referenced from an HTML comment
near the top of the root `README.md`. Keep it under ~10 MB so it loads on the README, and
scrub or use sandbox data — **never real company books**.
