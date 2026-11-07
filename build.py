"""Builds the studio's GitHub Pages site from site.json and games/<slug>/.

    python build.py

Writes index.html at the root and, per game, <slug>/index.html, <slug>/privacy.html and
<slug>/support.html. Commit the generated files too: GitHub Pages serves them as they are.

In the page sources (games/<slug>/*.html) these are filled in:
    $studio  the studio name (site.json)      $email  the support address (site.json)
    $game    the game's name (game.json)      $updated  the page's effective date (game.json)
Write a real dollar sign as $$.
"""
import html, json, os, shutil, string

ROOT = os.path.dirname(os.path.abspath(__file__))
site = json.load(open(os.path.join(ROOT, "site.json"), encoding="utf-8"))


def page(title, body, depth, desc="", icon=""):
    up = "../" * depth
    fav = f'<link rel="icon" href="{icon}">\n<link rel="apple-touch-icon" href="{icon}">\n' if icon else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="stylesheet" href="{up}style.css">
{fav}</head>
<body>
<header><a class="studio" href="{up}index.html">{html.escape(site["studio"])}</a></header>
<main>
{body}
</main>
<footer>&copy; {html.escape(site["studio"])} &middot; <a href="mailto:{site["email"]}">{site["email"]}</a></footer>
</body>
</html>
"""


def fill(text, game):
    return string.Template(text).substitute(
        studio=html.escape(site["studio"]), email=site["email"],
        game=html.escape(game["name"]), updated=game["updated"])


cards = []
for slug in site["games"]:
    src = os.path.join(ROOT, "games", slug)
    game = json.load(open(os.path.join(src, "game.json"), encoding="utf-8"))
    out = os.path.join(ROOT, slug)
    os.makedirs(out, exist_ok=True)
    links = []
    icon = ""
    if game.get("icon"):
        shutil.copyfile(os.path.join(src, game["icon"]), os.path.join(out, game["icon"]))
        icon = game["icon"]
    for kind, label in (("privacy", "Privacy policy"), ("support", "Support")):
        f = os.path.join(src, kind + ".html")
        if not os.path.exists(f):
            continue
        body = fill(open(f, encoding="utf-8").read(), game)
        nav = f'<p class="crumbs"><a href="index.html">{html.escape(game["name"])}</a></p>\n'
        title = "%s: %s" % (game["name"], label)
        open(os.path.join(out, kind + ".html"), "w", encoding="utf-8", newline="\n").write(
            page(title, nav + body, 1, game["tagline"], icon))
        links.append(f'<a class="button" href="{kind}.html">{label}</a>')
    stores = "".join(f'<a class="button ghost" href="{html.escape(u)}">{html.escape(n)}</a>'
                     for n, u in game.get("stores", {}).items() if u)
    head_img = f'<img class="app-icon" src="{icon}" alt="" width="96" height="96">' if icon else ""
    body = f"""{head_img}<h1>{html.escape(game["name"])}</h1>
<p class="lede">{html.escape(game["tagline"])}</p>
<p>{html.escape(game["blurb"])}</p>
<p class="row">{"".join(links)}{stores}</p>"""
    open(os.path.join(out, "index.html"), "w", encoding="utf-8", newline="\n").write(
        page(game["name"], body, 1, game["tagline"], icon))
    card_img = f'<img src="{slug}/{icon}" alt="" width="56" height="56">' if icon else ""
    cards.append(f"""<a class="card" href="{slug}/index.html">{card_img}
<strong>{html.escape(game["name"])}</strong>
<span>{html.escape(game["tagline"])}</span>
</a>""")

home = f"""<h1>{html.escape(site["studio"])}</h1>
<p class="lede">{html.escape(site["about"])}</p>
<h2>Our games</h2>
<div class="cards">
{chr(10).join(cards)}
</div>
<h2>Contact</h2>
<p>Questions, problems or feedback: <a href="mailto:{site["email"]}">{site["email"]}</a>. We usually answer within two working days.</p>"""
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8", newline="\n").write(page(site["studio"], home, 0, site["about"]))
print("built:", ", ".join(site["games"]))
