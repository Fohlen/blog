# Blog

Port of the old [Quarto](https://quarto.org) blog (`fohlen.github.io`) to [Hugo](https://gohugo.io)
with the [YinYang](https://github.com/joway/hugo-theme-yinyang) theme.

This README documents the process and conventions so future work stays consistent.
Read it before porting another post.

## Structure

```
blog/
├── content/
│   ├── about/                      # About page (index.md + profile image)
│   └── posts/<slug>/               # Hugo posts (index.md + images)
│       └── index.md
├── layouts/                        # Site-level overrides of theme templates
│   ├── _default/single.html        # author-as-string fix
│   └── index.html                  # posts list with flex categories
├── notebooks/<slug>/               # uv workspace sub-projects (notebook post sources)
│   ├── pyproject.toml              # per-post dependencies
│   ├── <Notebook>.ipynb            # notebook (committed WITHOUT outputs, see nbstripout)
│   └── <data> <images>             # files the notebook reads
├── static/css/custom.css           # theme overrides (loaded last)
├── themes/yinyang                  # theme git submodule (kept pristine)
├── hugo.toml
├── pyproject.toml                  # root uv workspace + tooling deps (nbconvert)
├── .gitattributes                  # Git LFS for images + nbstripout for *.ipynb
└── README.md
```

## Prerequisites

- `hugo` (extended)
- `git-lfs`
- `uv`
- `cwebp` (image conversion)
- `nbstripout` (installed via `uv tool install nbstripout`)
- Root venv: `uv sync` (provides `jupyter nbconvert`)

## uv workspaces (notebook sources)

The root `pyproject.toml` declares a uv workspace: `[tool.uv.workspace] members = ["notebooks/*"]`.
Every notebook-based post is its own sub-project in `notebooks/<slug>/` with its own
`pyproject.toml` listing that post's dependencies (converted from the original
`requirements.txt`, keeping the `~=` pins).

```bash
uv sync        # install root + all workspace members into .venv
```

## Porting a markdown post

The old post is `posts/<slug>/index.qmd`. Copy the content into
`content/posts/<slug>/index.md`:

- Keep the YAML front matter, but drop Quarto-only keys (`bibliography:`, `format:`).
- Skip the title/header image (the first image at the top of the post) and do not
  copy it. Keep inline content images.
- Convert kept images to webp (`cwebp -q 80`) and update the references.
- Citations: do NOT use Quarto `[see @key]` + `::: {#refs}`. Convert manually to
  `[see [N]](#refN)` and build a `### References` section by hand from the `.bib`,
  each entry prefixed with an anchor `<a id="refN"></a>`. (hugo-cite was evaluated
  but is too old for current Hugo — `getJSON`/`echoParam` were removed.)

## Porting a notebook post

Source of truth lives in the workspace; the rendered post is generated from it.

```bash
# 1. Set up the workspace sub-project
mkdir -p notebooks/<slug>
cp <source>/<Notebook>.ipynb <source>/<data> ... notebooks/<slug>/
# write notebooks/<slug>/pyproject.toml with [project] name, requires-python, dependencies

# 2. Render the post with figures (nbconvert embeds the stored chart outputs)
../../.venv/bin/jupyter nbconvert --to markdown <Notebook>.ipynb --output-dir ../../content/posts/<slug>/
```

Then tidy the generated output for Hugo:

1. Rename `<Notebook>.md` → `index.md`.
2. Clean the front matter: remove the Quarto `format:` / `jupyter:` keys, keep
   `title`/`description`/`author`/`date`/`categories`.
3. Remove the title/header image reference.
4. Move the chart PNGs out of `<Notebook>_files/` into the post folder and rewrite
   the `![png](<Notebook>_files/...)` references.
5. Optionally strip the Quarto `#| label:` / `#| fig-cap:` comment lines from code
   cells (they are only meaningful to Quarto).
6. Convert all images (including chart PNGs) to webp and update references. Keep
   vector diagrams (`*.svg`) as-is — don't rasterize them.
7. If the post links to helper scripts (e.g. `[computation](distances.py)`), copy them
   into the post folder too so the relative links resolve in the published site.
8. Heavy deps that are only needed to run the helper scripts (e.g. `mteb`, `spacy`)
   go in a `[project.optional-dependencies] scripts = [...]` group instead of the
   main `dependencies`, so `uv sync` stays light.
9. Interactive outputs (matplotlib `FuncAnimation` → `to_jshtml()`) do NOT survive the
   Hugo build: goldmark re-parses the embedded script as markdown and breaks it. Export
   the animation as an animated GIF instead (extract the base64 frames from the notebook
   output and assemble with `ffmpeg`), and drop the animation HTML from the post.

## Notebooks in git (keep the repo small)

Chart outputs are base64 blobs and would bloat the repo, so they are stripped at
commit time with **nbstripout**, installed as a git filter:

```bash
uv tool install nbstripout
nbstripout --install        # adds `*.ipynb filter=nbstripout` to .gitattributes
```

- Working copies keep the full outputs (so `nbconvert` can render figures).
- The committed `.ipynb` blob is stripped (e.g. 400 KB -> 28 KB).
- To re-apply after cloning or a reinstall: `uv tool install nbstripout && nbstripout --install`.

There is deliberately no `jupytext` — `nbconvert` alone renders the post, and
`nbstripout` keeps the committed `.ipynb` small. (jupytext pairing was considered
and dropped as redundant.)

## Images

- Git LFS tracks all image formats via `.gitattributes`
  (`*.jpg`, `*.png`, `*.webp`, `*.gif`, `*.svg`, `*.avif`, `*.bmp`, `*.tiff`).
- Post header/title images are skipped during porting.
- All content images are converted to webp (`cwebp -q 80`) — roughly halves size.
- Verify with `git lfs ls-files` and `git check-attr filter -- <file>`.

## Theme customizations (theme submodule is never edited)

Site overrides live in `layouts/` and `static/css/custom.css`:

- `layouts/_default/single.html` — the theme expected `author` front matter to be a
  dict (`.Params.author.homepage`), but posts use a plain string; the override
  handles both.
- `layouts/index.html` — homepage post list: replaced the narrow category grid
  column with a flex row (`.posts-title-row`: title left, categories right,
  wrapping with gaps).
- `static/css/custom.css` — system sans-serif body font (the theme's Bree Serif
  read as bold), `.about-portrait` (centered, circular profile image), flex
  category layout, and `extraHead` injects the old goatcounter/verification tags.
- `hugo.toml` → `params.extraHead` also loads KaTeX (CSS + `auto-render`), so
  LaTeX math (`$...$` / `$$...$$`) in posts renders; the theme has no math support.

## Verification

```bash
hugo              # builds; check for errors/warnings
hugo server       # preview
git lfs ls-files  # images are LFS pointers
git status        # ensure no huge files staged (check-attr ipynb)
```

## Porting status

- [x] `why-originality-matters` (markdown)
- [x] `python-dataclasses-a-package-full-of-surprises` (markdown, manual citations)
- [x] `yguard-release` (markdown)
- [x] `compression-based-classifier` (notebook, manual citations)
- [x] `missing-spacy-benchmark` (notebook, manual citations)
- [x] `network-randimisation` (notebook, manual citations, animations as GIFs)
- [x] `triton-grpc` (notebook)
- [x] `simulating-the-game-with-monte-carlo` (notebook, manual citations)
- [x] `linear-regression-l2-norm-dropout-relation` (notebook, manual citations)
- [x] `mapping-spans-between-documents-interview-question` (markdown)
- [x] `property-graph-db` (markdown, manual citations)
- [ ] `modeling_mindsets` (notebook — workspace set up, post in progress)
- [ ] remaining posts
