#!/usr/bin/env python3
"""Build the booking site and press kit from content.json.

Usage:
    ./build.py              # writes dist/
    ./build.py --out DIR    # writes DIR/

Standard library only. Static files in static/ are copied as-is; the two
pages (home + press kit) are rendered from content.json.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def e(value: object) -> str:
    return escape(str(value), quote=True)


def fmt_date(iso: str) -> tuple[str, str]:
    d = date.fromisoformat(iso)
    return d.strftime("%b").upper(), str(d.day)


# --------------------------------------------------------------------- pieces

def head(c: dict, title: str, description: str, base: str, canonical: str) -> str:
    site = c["site"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(canonical)}">
<link rel="icon" href="{base}assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{base}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{base}assets/css/site.css">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(canonical)}">
<meta property="og:image" content="{e(site['url'].rstrip('/') + '/' + site['og_image'])}">
<meta name="twitter:card" content="summary_large_image">
</head>"""


def header(c: dict, base: str) -> str:
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{base}"><img src="{base}{e(c['site']['logo_mark'])}" alt="" width="36" height="36">{e(c['site']['logo_text'])}</a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <a href="{base}#about">About</a>
      <a href="{base}#mixes">{e(c['mixes_section']['title'])}</a>
      <a href="{base}#dates">Dates</a>
      <a href="{base}press/">Press kit</a>
      <a class="btn btn-sm btn-primary" href="{base}#book">Book now</a>
    </nav>
  </div>
</header>"""


def socials(c: dict) -> str:
    links = "".join(
        f'<li><a href="{e(s["url"])}" rel="me noopener" target="_blank">{e(s["label"])}</a></li>'
        for s in c["socials"]
    )
    return f'<ul class="socials">{links}</ul>'


def footer(c: dict, base: str) -> str:
    site = c["site"]
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div>
      <p class="brand">{e(site['logo_text'])}</p>
      <p class="muted">{e(site['location'])}</p>
    </div>
    {socials(c)}
    <p class="muted small">Bookings: <a href="mailto:{e(c['contact']['booking_email'])}">{e(c['contact']['booking_email'])}</a></p>
  </div>
</footer>
<script src="{base}assets/js/site.js" defer></script>
</body>
</html>
"""


def stats(c: dict) -> str:
    items = "".join(
        f'<div class="stat"><span class="stat-value">{e(s["value"])}</span>'
        f'<span class="stat-label">{e(s["label"])}</span></div>'
        for s in c["stats"]
    )
    return f'<div class="stats">{items}</div>'


def genres(c: dict) -> str:
    return '<ul class="tags">' + "".join(f"<li>{e(g)}</li>" for g in c["genres"]) + "</ul>"


def mix_kind(m: dict, tag: str = "p") -> str:
    # small label like "Edit" or "Mix" so original work stands out
    return f'<{tag} class="mix-kind">{e(m["kind"])}</{tag}>' if m.get("kind") else ""


def mix_card(m: dict) -> str:
    if m.get("embed"):
        media = (
            f'<iframe src="{e(m["embed"])}" title="{e(m["title"])}" loading="lazy" '
            f'allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>'
        )
    else:
        media = (
            f'<a class="mix-link" href="{e(m["url"])}" target="_blank" rel="noopener">'
            f'<span class="play" aria-hidden="true"></span>Listen</a>'
        )
    return f"""<article class="mix">
  <div class="mix-bar" aria-hidden="true"><span></span><i>_</i><i>□</i><i>×</i></div>
  <div class="mix-media">{media}</div>
  {mix_kind(m)}
  <h3>{e(m['title'])}</h3>
  <p class="muted">{e(m['description'])}</p>
</article>"""


def dates_list(c: dict) -> str:
    today = date.today().isoformat()
    upcoming = sorted((d for d in c["dates"] if d["date"] >= today), key=lambda d: d["date"])
    if not upcoming:
        return '<p class="muted">No public dates right now. Want one in your city? <a href="#book">Book a date.</a></p>'
    rows = []
    for d in upcoming:
        mon, day = fmt_date(d["date"])
        link = (
            f'<a class="btn btn-sm" href="{e(d["url"])}" target="_blank" rel="noopener">Tickets</a>'
            if d.get("url") else ""
        )
        rows.append(
            f'<li class="date-row"><time datetime="{e(d["date"])}"><span>{mon}</span><b>{day}</b></time>'
            f'<div><p class="date-venue">{e(d["venue"])}</p><p class="muted">{e(d["city"])}</p></div>{link}</li>'
        )
    return '<ul class="dates">' + "".join(rows) + "</ul>"


def venues(c: dict) -> str:
    return '<ul class="venues">' + "".join(f"<li>{e(v)}</li>" for v in c["venues"]) + "</ul>"


def testimonials(c: dict) -> str:
    return '<div class="quotes">' + "".join(
        f'<figure class="quote"><blockquote>{e(t["quote"])}</blockquote>'
        f'<figcaption><b>{e(t["name"])}</b> <span class="muted">{e(t["role"])}</span></figcaption></figure>'
        for t in c["testimonials"]
    ) + "</div>"


def played_section(c: dict) -> str:
    # Hidden until there's something real to show; no filler venues.
    if not c["venues"] and not c["testimonials"]:
        return ""
    return f"""<section id="played" class="section">
  <div class="wrap">
    <h2>Played at</h2>
    {venues(c) if c["venues"] else ""}
    {testimonials(c) if c["testimonials"] else ""}
  </div>
</section>
"""


def options(values: list[str]) -> str:
    return "".join(f'<option value="{e(v)}">{e(v)}</option>' for v in values)


def booking_form(c: dict) -> str:
    b = c["booking"]
    return f"""<form class="booking-form" data-endpoint="{e(b['form_endpoint'])}" data-email="{e(c['contact']['booking_email'])}" novalidate>
  <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div>
  <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
  <div class="field"><label for="f-date">Event date</label><input id="f-date" name="event_date" type="date" required></div>
  <div class="field"><label for="f-type">Event type</label><select id="f-type" name="event_type" required><option value="">Choose one</option>{options(b['event_types'])}</select></div>
  <div class="field"><label for="f-venue">Venue and city</label><input id="f-venue" name="venue" required></div>
  <div class="field"><label for="f-guests">Expected guests</label><input id="f-guests" name="guests" type="number" min="1" inputmode="numeric"></div>
  <div class="field"><label for="f-hours">Set length</label><input id="f-hours" name="set_length" placeholder="e.g. 10pm to 2am"></div>
  <div class="field"><label for="f-budget">Budget</label><select id="f-budget" name="budget"><option value="">Choose one</option>{options(b['budget_ranges'])}</select></div>
  <div class="field field-wide"><label for="f-msg">Tell me about the event</label><textarea id="f-msg" name="message" rows="5" placeholder="Vibe, crowd, music you want (or don't want), equipment on site."></textarea></div>
  <div class="hp" aria-hidden="true"><label for="f-company">Leave this empty</label><input id="f-company" name="company" tabindex="-1" autocomplete="off"></div>
  <div class="field-wide form-actions">
    <button class="btn btn-primary" type="submit">Send booking request</button>
    <p class="form-status" role="status" aria-live="polite"></p>
  </div>
</form>"""


def contact_block(c: dict) -> str:
    ct = c["contact"]
    rows = [f'<li><span class="muted">Booking</span> <a href="mailto:{e(ct["booking_email"])}">{e(ct["booking_email"])}</a></li>']
    if ct.get("management_email"):
        who = f' ({e(ct["management_name"])})' if ct.get("management_name") else ""
        rows.append(f'<li><span class="muted">Management{who}</span> <a href="mailto:{e(ct["management_email"])}">{e(ct["management_email"])}</a></li>')
    if ct.get("phone"):
        rows.append(f'<li><span class="muted">Phone</span> <a href="tel:{e(ct["phone"])}">{e(ct["phone"])}</a></li>')
    return '<ul class="contact-list">' + "".join(rows) + "</ul>"


# ---------------------------------------------------------------------- pages

def home(c: dict) -> str:
    site, bio = c["site"], c["bio"]
    long_bio = "".join(f"<p>{e(p)}</p>" for p in bio["long"])
    mixes = "".join(mix_card(m) for m in c["mixes"])
    return f"""{head(c, f"{site['name']} | Bookings", bio['short'], "", site['url'])}
<body>
{header(c, "")}
<main id="main">

<section class="hero">
  <div class="wrap">
    <p class="eyebrow">{e(site['location'])}</p>
    <h1><img src="{e(site['banner'])}" alt="{e(site['name'])}" width="2000" height="419" fetchpriority="high"></h1>
    <p class="lede">{e(site['tagline'])}</p>
    <div class="actions">
      <a class="btn btn-primary" href="#book">Book a date</a>
      <a class="btn" href="press/">Press kit</a>
    </div>
  </div>
</section>

<section id="about" class="section">
  <div class="wrap split">
    <div>
      <h2>About</h2>
      {long_bio}
      {genres(c)}
    </div>
    <div>{stats(c)}</div>
  </div>
</section>

<section id="mixes" class="section">
  <div class="wrap">
    <h2>{e(c['mixes_section']['title'])}</h2>
    <p class="muted section-intro">{e(c['mixes_section']['intro'])}</p>
    <div class="mix-grid">{mixes}</div>
  </div>
</section>

{played_section(c)}
<section id="dates" class="section">
  <div class="wrap">
    <h2>Upcoming dates</h2>
    {dates_list(c)}
  </div>
</section>

<section id="book" class="section">
  <div class="wrap split">
    <div>
      <h2>Book {e(site['name'])}</h2>
      <p>House nights, hip hop nights, and everything in between: clubs, day parties, festivals, private events, and brand activations. Share the details and I'll follow up with availability and a quote.</p>
      <p class="muted">{e(c['contact']['response_time'])}</p>
      {contact_block(c)}
      <p><a href="press/">Promoters: grab the press kit</a> for bios, photos, and the tech rider.</p>
    </div>
    {booking_form(c)}
  </div>
</section>

</main>
{footer(c, "")}"""


def press(c: dict) -> str:
    site, bio, rider = c["site"], c["bio"], c["rider"]
    long_bio = "\n\n".join(bio["long"])
    photos = "".join(
        f'<figure class="photo"><img src="../{e(p["src"])}" alt="{e(p["alt"])}" loading="lazy">'
        f'<figcaption><span class="muted small">{e(p["credit"])}</span>'
        f'<a class="btn btn-sm" href="../{e(p["src"])}" download>Download</a></figcaption></figure>'
        for p in c["press_photos"]
    )
    logos = "".join(
        f'<figure class="logo-card{" logo-wide" if l.get("wide") else ""}"><img src="../{e(l["src"])}" alt="{e(l["label"])}" loading="lazy">'
        f'<figcaption><span class="small">{e(l["label"])}</span>'
        f'<a class="btn btn-sm" href="../{e(l["src"])}" download>Download</a></figcaption></figure>'
        for l in c["logos"]
    )
    tech = "".join(f"<li>{e(r)}</li>" for r in rider["technical"])
    hosp = "".join(f"<li>{e(r)}</li>" for r in rider["hospitality"])
    mixes = "".join(
        f'<li>{mix_kind(m, "span")} <a href="{e(m["url"])}" target="_blank" rel="noopener">{e(m["title"])}</a> <span class="muted">{e(m["description"])}</span></li>'
        for m in c["mixes"]
    )
    return f"""{head(c, f"{site['name']} | Press kit", f"Press kit for {site['name']}: bios, photos, tech rider, and booking contacts.", "../", site['url'].rstrip('/') + '/press/')}
<body class="press">
{header(c, "../")}
<main id="main">

<section class="section press-head">
  <div class="wrap">
    <p class="eyebrow">Electronic press kit</p>
    <h1>{e(site['name'])}</h1>
    <p class="lede">{e(site['tagline'])}</p>
    <div class="actions no-print">
      <button class="btn btn-primary" type="button" data-print>Save as PDF</button>
      <a class="btn" href="../#book">Book a date</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {stats(c)}
    {genres(c)}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="bio-block">
      <div class="bio-head"><h2>Short bio</h2><button class="btn btn-sm no-print" type="button" data-copy="bio-short">Copy</button></div>
      <p id="bio-short">{e(bio['short'])}</p>
    </div>
    <div class="bio-block">
      <div class="bio-head"><h2>Full bio</h2><button class="btn btn-sm no-print" type="button" data-copy="bio-long">Copy</button></div>
      <div id="bio-long" class="prewrap">{e(long_bio)}</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Press photos</h2>
    <p class="muted no-print">High resolution. Credit the photographer when you use them.</p>
    <div class="photo-grid">{photos}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Logos</h2>
    <p class="muted no-print">Use these on flyers and event pages. Keep them unaltered.</p>
    <div class="logo-grid">{logos}</div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    {f'<div><h2>Played at</h2>{venues(c)}</div>' if c["venues"] else ""}
    <div><h2>{e(c['mixes_section']['title'])}</h2><ul class="plain">{mixes}</ul></div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div><h2>Tech rider</h2><ul class="checklist">{tech}</ul></div>
    <div><h2>Hospitality</h2><ul class="checklist">{hosp}</ul></div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div><h2>Contact</h2>{contact_block(c)}</div>
    <div><h2>Socials</h2>{socials(c)}</div>
  </div>
</section>

</main>
{footer(c, "../")}"""


# ----------------------------------------------------------------------- main

def build(out: Path) -> None:
    content = json.loads((ROOT / "content.json").read_text())
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(ROOT / "static", out)
    (out / "index.html").write_text(home(content))
    (out / "press").mkdir()
    (out / "press" / "index.html").write_text(press(content))
    print(f"Built {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=ROOT / "dist")
    build(parser.parse_args().out.resolve())
