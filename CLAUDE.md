# CLAUDE.md

Notes for Claude Code (and other AI agents) working in this repo.

## Authorship: Tawaun only

Never list Claude as an author, co-author, or contributor anywhere in this repo.

- Before your first commit, set the git identity for this repo:
  `git config user.name "Tawaun Lucas"` and
  `git config user.email "86265976+tawaunl@users.noreply.github.com"`.
- No `Co-Authored-By: Claude`, `Claude-Session:`, or any other Claude trailer in commit messages.
- No "Generated with Claude Code" (or similar) line in PR titles, descriptions, or comments. Some PR tools append one automatically: after opening or editing a PR, re-read its description and remove it.

## Layout

- `content.json`: all site copy. Edit this, not the generated HTML.
- `build.py`: renders `dist/` from `content.json` and `static/` (standard library only).
- `static/`: CSS, JS, images, and brand assets copied into `dist/` as-is.
- `netlify.toml`: Netlify builds `python3 build.py` and publishes `dist/`. The live site is https://twonmixes.com.

## Before you finish a change

```bash
./build.py
python3 -m http.server -d dist 8000   # check http://localhost:8000 at desktop and phone widths
```

Netlify posts a deploy preview link on every PR.

## Copy and voice

- Don't use em dashes in site copy.
- House and hip hop are equal strengths; neither is secondary.
- Don't invent facts (gigs, venues, stats). Leave a TODO instead.
