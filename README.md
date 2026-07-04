# EcoPulse — Air Quality & Weather Intelligence for Uzbekistan

A Flask web application that shows live air quality (US EPA AQI) and
weather for all 14 regions of Uzbekistan, with user accounts and an
administrator panel.

## Features

- Landing page, registration and sign-in (passwords stored as salted hashes)
- Dashboard with a national overview card for every region
- Region pages: current weather, EPA AQI with health advice, a 48-hour
  temperature/PM2.5 chart, 7-day forecast and a six-pollutant breakdown
- Admin panel: total users, total administrators and a full user table
- CSRF-protected forms, role-based access control
- Data from the free Open-Meteo weather and air-quality APIs (no API key
  needed), cached for 10 minutes to stay inside free limits

## Run locally

```bash
python -m venv venv
venv\Scripts\activate        # Windows  (use `source venv/bin/activate` on macOS/Linux)
pip install -r requirements.txt
flask --app app run --debug
```

Open http://127.0.0.1:5000 — the SQLite database is created automatically.

**The first account you register automatically becomes the administrator.**
Promote more admins later with:

```bash
flask --app app create-admin someone@example.com
```

No internet connection? Run with demo data (clearly labelled in the UI):

```bash
# Windows PowerShell
$env:DEMO_DATA="1"; flask --app app run --debug
```

## Deploy for free (Render)

1. Push this folder to a GitHub repository.
2. Go to https://render.com → New → Blueprint → pick your repo.
   Render reads `render.yaml` and configures everything.
3. Click **Deploy**. Your app gets a public `https://….onrender.com` URL.

Note: on the free tier the SQLite file resets when the service restarts.
For persistent accounts, create a free PostgreSQL instance on Render and
set its connection string as the `DATABASE_URL` environment variable —
no code changes needed.

## Accuracy, honestly

Forecasts come from Open-Meteo, which blends the Copernicus CAMS
atmospheric model with leading national weather models — the same class
of sources commercial weather apps use. No provider on Earth offers 100%
accurate forecasts; that is a physical limit of the atmosphere, not a
software bug. This app therefore reports the official EPA AQI categories
that health agencies designed to be robust to normal forecast error.

## Project layout

```
app.py           Flask app factory, CSRF protection, error pages, CLI
config.py        Environment-driven configuration
extensions.py    Shared SQLAlchemy / LoginManager instances
models.py        User model
auth.py          Register / login / logout routes
views.py         Landing, dashboard and region pages
admin.py         Admin-only panel
services/        Open-Meteo client, EPA AQI maths, region catalogue
templates/       Jinja2 templates
static/          Stylesheet and chart script
```
