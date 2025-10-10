# Urban Mobility

A Flask backend for the Urban Mobility project.

This README shows how to set up and run the Flask application locally after cloning the repository.

## Prerequisites

- Python 3.8 or newer. Verify with:

```bash
python3 --version
```

- Git


## Quick start

1. Clone the repository and change into the project directory:

```bash
git clone https://github.com/agmbabazi/urban_mobility.git
cd urban_mobility
```

2. Create and activate a virtual environment (recommended):

On Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell):

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application in development mode:

Change to the backend directory

```bash
python3 app.py
```

Visit the server at http://127.0.0.1:5000

## Project layout

- `backend/app.py` — application entrypoint (creates Flask app and registers routes)
- `backend/routes/routes.py` — HTTP route handlers
- `backend/models/models.py` — data models and helpers
- `requirements.txt` — Python dependencies

Adjust paths above if your files are located elsewhere.

## Environment variables

Set environment variables before running the app. Common variables:

If you need to store secrets (API keys, DB URIs), prefer using a `.env` file and `python-dotenv` to load them in development.

## Common commands

- Run the app directly with Python (alternative to `flask run`):

```bash
python3 backend/app.py
```

- Install a new dependency and update `requirements.txt`:

```bash
pip install <package>
pip freeze > requirements.txt
```

## Testing

There are no automated tests included yet. To add tests, create a `tests/` directory and use `pytest`.

## Troubleshooting

- "Module not found" errors: ensure your virtual environment is active and dependencies are installed.
- Port already in use: run `flask run --port <other-port>` or stop the process using the port.
- Debugger not showing detailed errors: set `FLASK_ENV=development` (do not enable in production).

