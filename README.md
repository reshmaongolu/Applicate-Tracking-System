# Applicant Tracking System

A simple Python-based applicant tracking system (ATS) with:

- SQLite storage for candidates, job postings, and applications
- CLI commands for adding candidates, jobs, and submitting applications
- Search and listing features
- Unit tests for core business logic

## Setup

```bash
python -m venv .venv
source .venv/Scripts/activate    # Windows
pip install -r requirements.txt
```

## Run

```bash
python -m app.main
```

Or after installing the package:

```bash
nats
```

## Web Frontend

Start the web app locally:

```bash
python -m app.web
```

Then open:

```text
http://127.0.0.1:5000
```

## Example Commands

```bash
python -m app.main add-candidate --name "Jane Doe" --email jane@example.com --skills Python Java
python -m app.main add-job --title "Backend Engineer" --department Engineering
python -m app.main submit-application --candidate-id 1 --job-id 1
python -m app.main list-applications
```
