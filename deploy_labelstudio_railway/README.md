# Minimal Label Studio deploy (Railway)

This folder is intentionally minimal.

## What to deploy
Point Railway **Root Directory** to this folder: `deploy_labelstudio_railway`.

## Files
- `requirements.txt` installs Label Studio only
- `start.sh` starts Label Studio on `0.0.0.0:$PORT`
- `.mise.toml` pins Python to 3.10

## Environment variables (Railway)
- `PORT` is provided by Railway
- Optional:
  - `LABEL_STUDIO_DATA_DIR` (e.g. `/app/.data`)
  - `LABEL_STUDIO_USERNAME`
  - `LABEL_STUDIO_PASSWORD`
