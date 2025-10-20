### Urban Mobility

## About the project
urban mobility is a web based application that it's purpose is to analyze, visualize, and explore the taxi trip data in New York City. This app uses a flask backend API and a static HTML, CSS, and JS for the fronted.

  . The frontend dashboard is http://127.0.0.1:5500/frontend/dashboard.html
  
  . And the backend server runs on http://127.0.0.1:5000

## features
. A dashboard that shows trip statistics

. RESTful APIs to fetche and summarize trip data

. Using SQLAlchemy for integration with the SQLite database

. Clean backend structure

. Fetching requests from the frontend to the backend APIs

. Dataset following NYC taxi public dataser schema


#A Flask backend for the Urban Mobility project.

This shows how to set up and run the Flask application locally after cloning the repository.

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

## Dataset Descriptions

# Column explanations

1. trip_id: Trip identification number.
2. pickup_datetime(pickup_ts): The date and time when the meter was engaged(started).
3. dropoff_datetime(dropoff_ts): The date and time when the meter was disengaged(stopped).
4. Passenger_count: Number of passengers in the vehicle (It is entered by the driver).
5. pickup_lat : Latitude coordinate where the trip began (pickup location).
6. pickup_lng : Longitude coordinate where the trip began(pickup location).
7. dropoff_lat : Latitude where the trip ended (dropoff location).
8. dropoff_lng : Longitude where the trip ended (dropoff location).
9. distance_km : total distance traveled for the whole trip. (trip distance)   
10. duration_min : time calculated from the dropoff and pickup time.
11. Fare_amount: The mount calculated by a meter based on time and distance.
12. tip_amount: The tip amount given by the passenger, not charged from the fare.


## Data transformationeady in use: run `flask run --port <other-port>` or stop the process using the port.
- Debugger not showing detailed errors: set `FLASK_ENV=development` (do not enable in production
