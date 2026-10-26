# DJ booking site and press kit

A static site with two pages:

- **Home** (`/`): hero, about, mixes, venues and testimonials, upcoming dates, and a booking request form.
- **Press kit** (`/press/`): copyable short and full bios, downloadable press photos, tech rider, hospitality, and contacts. The "Save as PDF" button prints a clean one-sheet.

## Edit content

All copy lives in [`content.json`](content.json). Replace every `TODO` and the `DJ NAME` placeholders, then rebuild.

- **Photos:** drop files into `static/assets/img/` and point `hero_image` and `press_photos[].src` at them.
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

`.github/workflows/pages.yml` builds and deploys to GitHub Pages on every push to `main`. Turn it on once under **Settings > Pages > Source: GitHub Actions**.
