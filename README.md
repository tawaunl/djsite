# TWON: booking site and press kit

A static site with two pages:

- **Home** (`/`): hero, about, mixes, venues and testimonials, upcoming dates, and a booking request form.
- **Press kit** (`/press/`): copyable short and full bios, downloadable press photos, tech rider, hospitality, and contacts. The "Save as PDF" button prints a clean one-sheet.

## Edit content

All copy lives in [`content.json`](content.json). Replace every `TODO` and the `DJ NAME` placeholders, then rebuild.

- **Photos and logos:** brand files live in `static/assets/img/brand/`. `site.banner` is the hero art, `site.logo_mark` the menu icon, and `logos` lists the press kit downloads. Press photos go in `press_photos`.
- **Mixes:** set `embed` to a SoundCloud or Mixcloud player URL (the `src` from their embed code) to show an inline player. Leave it empty to show a "Listen" link instead.
- **Dates:** past dates hide automatically on each build.
- **Booking form:** with `booking.form_endpoint` empty, the form opens the visitor's email app with the request filled in. Paste a [Formspree](https://formspree.io) form URL there to receive requests without that step.

## Build and preview

```bash
./build.py
python3 -m http.server -d dist 8000   # open http://localhost:8000
```

Python 3.9+ standard library only. Output goes to `dist/` (not committed).

## Deploy

The live site is **https://twonmixes.com**, hosted on Netlify. `netlify.toml` tells Netlify to run `python3 build.py` and publish `dist/`, so every push to `main` redeploys automatically.

`.github/workflows/pages.yml` also publishes a copy to GitHub Pages. Every page's canonical link points at twonmixes.com, so search engines treat the Netlify site as the real one.
