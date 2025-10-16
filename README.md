### Urban Mobility

## Dataset Descriptions

# Column explanations

ID: Trip identification number
1. VendorID: A code indicating the TPEP(Taxicab Passenger Enhancement Program) provider that provided the record. 
2. tpep_pickup_datetime: The date and time when the meter was engaged(started).
3. tpep_dropoff_datetime: The date and time when the meter was disengaged(stopped).
4. Passenger_count: Number of passengers in the vehicle (It is entered by the driver).
5. Trip_distance: The total trip distance in miles reported by the taximeter.
6. PULocationID: TLC(Taxi and Limousine Commission) Taxi Zone where the meter was engaged.
7. DOLocationID: TLC Taxi Zone where the meter was disengaged.
8. RateCodeID: The final rate code in effect at the end of the trip.
       a. 1= Standard rate
       b. 2=JFK
       c. 3=Newark
       d. 4=Nassau or Westchester
       e. 5= Negotiated fare
       f. 6=Group ride    
9. Store_and_fwd_flag: It indicates whether the trip record was stored in the vehicle memory before being sent to the vendor,due to the vehicle not have a connection to the server.
       "Y" for store and forward trip
       "N" for not store and forward trip
10. Payment_type: A numeric code signifying how the passenger paid for the trip.
       a. 1 = Credit card
       b. 2 = Cash
       c. 3 = No charge
       d. 4 = Dispute
       e. 5 = Unknown
       f. 6 = Voided trip
11. Fare_amount: The mount calculated by a meter based on time and distance.
12. Extra: Miscellaneous extras and surcharges. Currently, this only includes the $0.50 and $1 rush hour and overnight charges.
13. MTA_tax: $0.50 MTA tax that is automatically triggered based on the metered rate in use.
14. Improvement_surcharge: $0.30 improvement surcharge assessed trips at the flag drop. The improvement surcharge began being levied in 2015.
15. Tip_amount: This field is automatically populated for credit card tips. Cash tips are not included
16. Tolls_amount: Total amount of all tolls paid in trip.
17. Total_amount: The total amount charged to passengers. Does not include cash tips.
18. congestion_surcharge: A congestion fee applied to trips that enter, leave, or travel within Manhattan south of 96th Street.Introduced in February 2019 to reduce traffic congestion.
19. Airport_fee: A flat surcharge automatically applied to trips to or from JFK and LaGuardia Airports.
20. cbd_congestion_fee: An additional charge related to the Central Business District (CBD) congestion pricing program.

## Data transformation

# Importing libraries
import pandas as pd 
import numpy as np 
from pathlib import Path 

pd.options.display.max_columns = None
pd.options.display.width = 120

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

