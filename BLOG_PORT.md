# Blog

Hugo blog (`fohlen.github.io`) using the [YinYang](https://github.com/joway/hugo-theme-yinyang)
theme. This documents the conventions for creating new posts.

## Prerequisites

- `hugo` (extended)
- `git-lfs`
- `uv`
- `cwebp` (image conversion)
- `nbstripout` (installed via `uv tool install nbstripout`)
- Root venv: `uv sync` (provides `jupyter nbconvert`)

## Creating a markdown post

Create `content/posts/<slug>/index.md`:

- Front matter: `title`, `description`, `author` (plain string), `date`, `categories`.
- Citations: use `[see [N]](#refN)` and build a `### References` section by hand,
  each entry prefixed with an anchor `<a id="refN"></a>`.

## Creating a notebook post

Source of truth lives in a uv workspace sub-project; the rendered post is generated from it.

```bash
# 1. Set up the workspace sub-project
mkdir -p notebooks/<slug>
cp <Notebook>.ipynb <data> <images> ... notebooks/<slug>/
# write notebooks/<slug>/pyproject.toml with [project] name, requires-python, dependencies
#   heavy deps only needed by helper scripts go in [project.optional-dependencies] scripts = [...]

# 2. Render the post with figures (nbconvert embeds the stored chart outputs)
../../.venv/bin/jupyter nbconvert --to markdown <Notebook>.ipynb --output-dir ../../content/posts/<slug>/
```

Then tidy the output for Hugo:

1. Rename `<Notebook>.md` → `index.md`.
2. Clean the front matter: keep only `title`/`description`/`author`/`date`/`categories`.
3. Move the chart PNGs out of `<Notebook>_files/` into the post folder and rewrite
   the `![png](<Notebook>_files/...)` references.
4. Convert all images (including chart PNGs) to webp (`cwebp -q 80`) and update
   references. Keep vector diagrams (`*.svg`) as-is — don't rasterize them.
5. If the post links to helper scripts (e.g. `[computation](distances.py)`), copy them
   into the post folder too so the relative links resolve in the published site.
6. Interactive outputs (matplotlib `FuncAnimation` → `to_jshtml()`) do NOT survive the
   Hugo build: goldmark re-parses the embedded script as markdown and breaks it. Export
   the animation as an animated GIF instead, and drop the animation HTML from the post.

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

## Images

- Git LFS tracks all image formats via `.gitattributes`
  (`*.jpg`, `*.png`, `*.webp`, `*.gif`, `*.svg`, `*.avif`, `*.bmp`, `*.tiff`).
- All content images are converted to webp (`cwebp -q 80`) — roughly halves size.
- Verify with `git lfs ls-files` and `git check-attr filter -- <file>`.

## Theme customizations (theme submodule is never edited)

Site overrides live in `layouts/` and `static/css/custom.css`. `hugo.toml` →
`params.extraHead` loads KaTeX (CSS + `auto-render`), so LaTeX math (`$...$` /
`$$...$$`) in posts renders; the theme has no math support.

## Verification

```bash
hugo              # builds; check for errors/warnings
hugo server       # preview
git lfs ls-files  # images are LFS pointers
git status        # ensure no huge files staged (check-attr ipynb)
```
