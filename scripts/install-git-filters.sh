#!/bin/sh
# One-time per-clone setup for the nbstripout git filter.
# Requires the repo venv to exist (uv sync).
set -e
git config filter.nbstripout.clean '.venv/bin/python -m nbstripout'
git config filter.nbstripout.smudge 'cat'
git config filter.nbstripout.required 'true'
git config diff.ipynb.textconv '.venv/bin/python -m nbstripout -t'
