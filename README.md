# Minimal PWA Flask App

A tiny Progressive Web App with a Flask backend and Supabase logging. Users enter a custom ID, view static content, and visits are recorded.

## Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# create .env with SUPABASE_URL and SUPABASE_API_KEY
python api/index.py
```

## Supabase Setup

Run the SQL schema in your project:

```bash
psql "$SUPABASE_DB" < sql/schema.sql
```

## Environment Variables

For local dev and Vercel deployment set:

- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY` (server side only)

## Deploying to Vercel

1. Push this repo to GitHub.
2. In Vercel, import the project.
3. Add the environment variables above.
4. Deploy.

## PWA Install

Open the site on Android Chrome or iOS Safari and use “Add to Home Screen.” The app works offline and launches without browser chrome.

## Privacy

The app stores the typed ID and visit timestamps in Supabase. No other personal data is collected.
