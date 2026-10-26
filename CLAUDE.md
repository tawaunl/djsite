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

## About TWON

- **Who:** Tawaun, DJing as **TWON**. Based in San Francisco.
- **Sound:** open format, and he excels at both **house** (house, tech house, afro house) and **hip hop** (hip hop, R&B, West Coast, throwbacks). The crossover between them is his edge. Expect more house, tech house, and afro house bookings in SF, but never frame hip hop as secondary.
- **Original work:** remixes, edits, and flips, shown on the site as "Mixes & Flips". Examples: House Every Weekend (TWON x BRWDY Edit), and the **DEEP CUTZ** mix series (first one: YG, "YG Quick Cutz").
- **Links:** Instagram [@twonmixes](https://instagram.com/twonmixes), [Linktree](https://linktr.ee/twoninthemix), [SoundCloud](https://soundcloud.com/twon_online/tracks) (display name T-WON), [YouTube](https://youtube.com/@twoninthemix). Booking: twoninthemix@gmail.com.
- **Instagram bio:** "Vibes Curator 🕴🏾 / Festival Lover / Open format | SF based📍 / Follow along for the journey 🕺🏾"

## Brand

- **Colors:** teal `#50d6db` (primary: buttons, links) and gold `#f2b544` (highlights: stats, labels), on a near-black background. Both come from the logos in `static/assets/img/brand/`.
- **Look:** old-school computer and early-2000s internet nostalgia, like retro file-transfer windows ("TWON has sent you a file 📁"). Use it for promo visuals and playful touches, not body text.

## Writing style

### Site copy (promoters read this)

- Clear, confident, and direct. A little of his voice is welcome ("songs ya had to be there for"), but keep it readable for a promoter or venue booker.
- Don't use em dashes. Use commas, periods, or colons.
- House and hip hop are equal strengths; neither is secondary.
- Don't invent facts (gigs, venues, residencies, stats, quotes). Leave a TODO instead.

### Captions and DJ posts (@twonmixes, SoundCloud and YouTube descriptions)

- **Short and playful.** Punchy line breaks, one idea per line.
- **Shape:** hook line, what it is, a quick vibe line, a call to action, "link in bio", then hashtags.
- **Slang, used naturally:** ya, y'all, hella, bruh, lit, crew, squad, szn, vibez, drip, forsure. Stretch words for hype ("Squaaaaad!", "killllllled ittt").
- **Punctuation:** lots of ellipses (".." "..." "....."), exclamation points, and sometimes a space before punctuation ("Until next time !").
- **Emojis:** sparing, sometimes doubled for emphasis (🔥🔥). Use the brown skin tone on hand and people emojis (✌🏾 🙌🏾 💪🏾 🤙🏾 🕺🏾).
- **Hashtags** only at the very end, never mid-caption. Casual posts can skip them.
- **Event recaps** open with excitement ("Wow! What a weekend!", "Bruh, what a week!") and close with a sign-off ("Another one for the books", "Until next time 🙌🏾", "See you again next year!").
- **Shoutouts** name each person's role: "Shout out to @x for spinning the music and keeping the vibes", "Huge thanks to @x", "Major shoutout", "Really big ups to @x".
- No em dashes here either.

Reference caption (the DEEP CUTZ: YG drop):

```
TWON has sent you a file 📁
DEEP CUTZ: YG is out now. Songs ya had to be there for!
Quick cuts.
AIM me after you listen. YT Link in bio 🔗
#DeepCutz #YG #Bompton #JerkinEra #WestCoastHipHop
```

"AIM me after you listen" was only for the YG mix. Don't reuse it on other posts; write a fresh call to action each time.
