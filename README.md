# saster-he.github.io

The personal academic website of Jie He, a biostatistics PhD student at Boston University: <https://saster-he.github.io/>.

It is a small [Hugo](https://gohugo.io/) site with hand-written templates. There is no theme, no JavaScript framework and no build step besides Hugo. GitHub Actions builds and publishes it on every push to `main` (see `.github/workflows/publish.yaml`).

## Run it locally

Install Hugo **0.136.5 extended** (the version the deploy uses), then from the repository root:

```sh
hugo server
```

and open <http://localhost:1313/>. `hugo --minify` writes the finished site to `public/`.

## Where things live

```
config/_default/      site settings: hugo.yaml, params.yaml (email and profile links), menus.yaml (the nav)
content/              the words: _index.md (Home), education.md, research.md, experience.md, cv.md, project/
layouts/              HTML templates (baseof, single, list, 404, Home) and partials (nav, footer, photo, score, entries)
assets/css/main.css   all styles, light and dark
assets/js/score.js    the score player on Home (the only script file)
assets/images/        the two portrait photos; Hugo makes the resized WebP versions at build time
static/fonts/         Source Serif 4 and IBM Plex Mono (WOFF2) with their licences
static/music/         the recording and the engraved score shown on Home
data/bwv846.json      timing data that keeps the score in step with the recording
tools/score/          offline scripts that produced the music files (not used by the build)
```

Education, Research and Experience entries are listed in the front matter of each page (`title`, `org`, `dates`, `text`, and an optional `link`). Edit them there.
A page can also set `lead` (an opening paragraph) and `entries_title` (a heading above the entries, as on Research). Home takes `name_zh` and `role` from `content/_index.md`.

## Music

The Home page plays J. S. Bach's Prelude in C major, BWV 846, from *The Well-Tempered Clavier*, Book I.

- Recording: Kimiko Ishizaka, from the [Open Well-Tempered Clavier](https://welltemperedclavier.org/), released into the public domain under CC0.
- Notes: Bach's, in the public domain.
- Score: re-engraved with Verovio from a MuseScore transcription, with one missing bar restored.

To rebuild the score, the timing data or the audio file, follow `tools/score/README.md`.

## Fonts

- [Source Serif 4](https://github.com/adobe-fonts/source-serif) by Adobe, SIL Open Font License 1.1 (`static/fonts/OFL-source-serif-4.txt`).
- [IBM Plex Mono](https://github.com/IBM/plex) by IBM, SIL Open Font License 1.1 (`static/fonts/OFL-ibm-plex-mono.txt`).

Both are the Latin subsets published by [Fontsource](https://fontsource.org/), copied unchanged.

## Licence

`LICENSE.md` is the MIT licence that came with the original Hugo Blox template this site started from.
