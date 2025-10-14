# %%
# Importing libraries
import pandas as pd 
import numpy as np 
from pathlib import Path 

pd.options.display.max_columns = None
pd.options.display.width = 120

# %%
# Loading the dataset
file_path = Path(r"C:\Users\ishim\urban_mobility\data\yellow_tripdata_2025-08.parquet")

# %%
# Reading the dataset
data = pd.read_parquet(file_path)

# %%
# Printing the dimensions of my dataset
print("Original shape", data.shape)

# %%
# Data inspection
data.info()

# %%
# Selecting columns  with numbers ?(floats and integers)
numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns

# %%
# Replacing the missing values with 0 to prevent errors when calculating
data[numeric_columns] = data[numeric_columns].fillna(0)

# %%
# Verifying if date and times are stored in the correct datetime format
for current_column in ['tpep_pickup_datetime', 'tpep_dropoff_datetime']:
    data[current_column] = pd.to_datetime(data[current_column], errors='coerce')

# %%
# Calculating the trip duration
trip_duration = data['tpep_dropoff_datetime'] - data['tpep_pickup_datetime'] 

# %%
# Converting trip duration into minutes and converting negative or null durations to 0
data['trip_duration_min'] = (
    (data['tpep_dropoff_datetime'] - data['tpep_pickup_datetime']).dt.total_seconds() / 60).fillna(0)

# %%
# Define all fare components
fare_components = ['fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge', 'congestion_surcharge', 'Airport_fee']

# Check if all columns exist and replace them with 0 if not
for column in fare_components:
    if column not in data.columns:
        data[column] = 0


# %%
# Manually calculate the total fare amount for all components
data['calculated_total_amount'] = data[fare_components].sum(axis=1)

# %%
# Compare the calculated total with the generated total_amount column
tolerance = 5 # It will allow a difference of 5 cents
data['difference'] = abs(data['total_amount'] - data['calculated_total_amount'])

# %%
# Rows where the difference is greater than the tolerance
mismatched_totals = data['difference'] > tolerance


# %%
clean_data = data[
    (data['trip_distance'] > 0) &
    (data['trip_duration_min'] > 0)
].copy()


# %%
clean_data = clean_data[
    (clean_data['trip_duration_min'] < 240) &  # < 4 hours
    (clean_data['trip_distance'] < 100)        # < 100 miles
]


# %%
clean_data['speed_mph'] = clean_data['trip_distance'] / (clean_data['trip_duration_min'] / 60)

# %%
# Additional cleaning filters

# Remove trips with zero or extremely high passenger counts
clean_data = clean_data[
    (clean_data['passenger_count'] > 0) &
    (clean_data['passenger_count'] <= 6)  # realistic upper bound
]

# Remove invalid or unknown payment types
valid_payment_types = [1, 2, 3, 4, 5, 6]  # standard NYC Taxi codes
clean_data = clean_data[clean_data['payment_type'].isin(valid_payment_types)]

# Drop rows with missing pickup or dropoff locations
clean_data = clean_data.dropna(subset=['PULocationID', 'DOLocationID'])

# Remove outliers in fare or tip amounts (e.g., extreme high values)
clean_data = clean_data[
    (clean_data['fare_amount'].between(1, 500)) &
    (clean_data['tip_amount'].between(0, 200))
]

# Optionally remove forwarded trips if not needed
clean_data = clean_data[clean_data['store_and_fwd_flag'] != 'Y']

print("Final cleaned shape:", clean_data.shape)



