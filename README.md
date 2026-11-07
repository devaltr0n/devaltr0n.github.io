# Tiny Hearth site

Tiny Hearth's GitHub Pages site (account `tinyhearth`, so `https://tinyhearth.github.io/`): a home page listing every game, and per game a page, a privacy
policy and a support page. Store listings link to `<site>/<game>/privacy.html` and
`<site>/<game>/support.html`.

## Change the studio name or email

Edit `site.json`, then run `python build.py` and commit everything (the generated `.html`
files included).

## Add a game

1. Copy `games/furry-roll/` to `games/<new-slug>/`.
2. Edit its `game.json` (name, tagline, blurb, effective date, store links) and rewrite
   `privacy.html` and `support.html` for what that game really does.
3. Add the slug to `"games"` in `site.json`, then run `python build.py`.

In the page sources `$studio`, `$email`, `$game` and `$updated` are filled in. Write `$$` for a
dollar sign.

## Publish on GitHub Pages

1. Create the studio's GitHub account and a **public** repository named
   `<account>.github.io` (the site is then at `https://<account>.github.io/`).
2. Push this folder to it.
3. In the repository: Settings > Pages > Build and deployment: Deploy from a branch, `main`,
   `/ (root)`.
4. After a minute the pages are live, for example
   `https://<account>.github.io/furry-roll/privacy.html`.

`.nojekyll` tells GitHub to serve the files as they are.
