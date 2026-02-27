# FounderOS — Startup Validation & Risk Intelligence Platform

A Django 5+ MVP for early-stage founders to validate ideas, analyze risks, and discover government funding.

## Quick Start

### 1. Set Up Environment

```bash
python -m venv venv
.\venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your values:

```
SECRET_KEY=your-secret-key
DEBUG=True
GEMINI_API_KEY=your-gemini-api-key   # Optional — works without it
```

### 3. Run Migrations & Setup

```bash
python manage.py migrate
python setup.py         # Creates admin user + seeds sample data
```

### 4. Start the Server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000**

## Login Credentials

- **Admin Panel**: http://127.0.0.1:8000/admin — `admin` / `admin123`

## Features

| Feature       | URL            | Description                 |
| ------------- | -------------- | --------------------------- |
| Landing Page  | `/`            | Public intro & CTA          |
| Dashboard     | `/dashboard/`  | Central control panel       |
| Pitch Lab     | `/pitches/`    | AI pitch analysis           |
| Risk Analysis | `/risk/`       | SWOT + risk scores          |
| Gov Schemes   | `/schemes/`    | Scheme eligibility matching |
| Doc Verify    | `/validation/` | Document validation         |
| Matching      | `/matching/`   | Mentor/Investor matches     |
| Profile       | `/profile/`    | Founder profile             |

## REST API

| Endpoint               | Method | Description       |
| ---------------------- | ------ | ----------------- |
| `/api/pitch/generate/` | POST   | AI pitch analysis |
| `/api/risk/analyze/`   | POST   | Risk assessment   |
| `/api/schemes/match/`  | POST   | Scheme matching   |

## Architecture

```
founderos/
├── accounts/     # Auth + FounderProfile
├── pitches/      # AI pitch analysis
├── risk/         # Risk scoring + SWOT
├── schemes/      # Gov scheme matching
├── matching/     # Mentor/investor matching
├── validation/   # Document verification
├── templates/    # Django HTML templates
├── static/       # CSS/JS assets
├── founderos/
│   ├── settings.py
│   ├── urls.py
│   └── ai_service.py  # Gemini AI wrapper
└── manage.py
```

## AI Integration

Powered by **Google Gemini 1.5 Flash**. Set `GEMINI_API_KEY` in `.env`.

Without an API key, all AI features return realistic **demo/placeholder** data so the app is fully functional for testing.

## Tech Stack

- **Backend**: Django 5+, Django REST Framework
- **Database**: SQLite (dev)
- **Frontend**: Django Templates + Tailwind CSS (CDN)
- **AI**: Google Gemini API (`google-generativeai`)
