# create_table.py
from sqlalchemy import create_engine, types
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

table_name = 'yellow_tripdata_2025_08'

dtype_mapping = {
    'VendorID': types.Integer(),
    'tpep_pickup_datetime': types.DATETIME(),
    'tpep_dropoff_datetime': types.DATETIME(),
    'passenger_count': types.Integer(),
    'trip_distance': types.Float(),
    'RatecodeID': types.Integer(),
    'store_and_fwd_flag': types.String(1),
    'PULocationID': types.Integer(),
    'DOLocationID': types.Integer(),
    'payment_type': types.Integer(),
    'fare_amount': types.Float(),
    'extra': types.Float(),
    'mta_tax': types.Float(),
    'tip_amount': types.Float(),
    'tolls_amount': types.Float(),
    'improvement_surcharge': types.Float(),
    'congestion_surcharge': types.Float(),
    'Airport_fee': types.Float(),
    'total_amount': types.Float(),
    'calculated_total_amount': types.Float(),
    'trip_duration_min': types.Float(),
    'speed_mph': types.Float(),
    'fare_per_mile': types.Float(),
    'tip_pct': types.Float(),
    'idle_trip_flag': types.Integer()
}

# SQLAlchemy engine
engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)
