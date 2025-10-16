from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pathlib import Path
from datetime import datetime
from sqlalchemy import func
from models.models import TripModel,db

# Initialize app and DB
app = Flask(__name__)
api = Api(app)

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR.parent / "sqlite" / "data.db"

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Resources
class Trip(Resource):
    def get(self):
        start = request.args.get("start")
        end = request.args.get("end")
        min_distance = request.args.get("min_distance")

        try:
            limit = int(request.args.get("limit", 20))
        except:
            limit = 20

        try:
            page = int(request.args.get("page", 1))
        except:
            page = 1

        offset = (page - 1) * limit

        query = TripModel.query

        if start:
            try:
                start_date = datetime.strptime(start, "%Y-%m-%d")
                query = query.filter(func.date(TripModel.pickup_datetime) >= start_date)
            except ValueError:
                pass

        if end:
            try:
                end_date = datetime.strptime(end, "%Y-%m-%d")
                query = query.filter(func.date(TripModel.pickup_datetime) <= end_date)
            except ValueError:
                pass

        if min_distance:
            try:
                min_dist = float(min_distance)
                query = query.filter(TripModel.distance_km >= min_dist)
            except ValueError:
                pass

        total = query.count()
        trips = query.offset(offset).limit(limit).all()

        def to_dict(trip):
            return {
                "id": trip.trip_id,
                "pickup_ts": trip.pickup_datetime.isoformat() if trip.pickup_datetime else None,
                "dropoff_ts": trip.dropoff_datetime.isoformat() if trip.dropoff_datetime else None,
                "pickup_lat": trip.pickup_lat,
                "pickup_lng": trip.pickup_lng,
                "dropoff_lat": trip.dropoff_lat,
                "dropoff_lng": trip.dropoff_lng,
                "fare_amount": trip.fare_amount,
                "tip_amount": trip.tip_amount,
                "distance_km": trip.distance_km,
                "duration_min": trip.duration_min,
                "passenger_count": trip.passenger_count,
            }

        return jsonify({
            "rows": [to_dict(t) for t in trips],
            "total": total
        })
    
class TripDetail(Resource):
    def get(self, trip_id):
        trip = TripModel.query.get(trip_id)

        if not trip:
            return jsonify({"error": "Trip not found"}), 404

        return jsonify({
            "id": trip.trip_id,
            "pickup_ts": trip.pickup_datetime.isoformat() if trip.pickup_datetime else None,
            "dropoff_ts": trip.dropoff_datetime.isoformat() if trip.dropoff_datetime else None,
            "pickup_lat": trip.pickup_lat,
            "pickup_lng": trip.pickup_lng,
            "dropoff_lat": trip.dropoff_lat,
            "dropoff_lng": trip.dropoff_lng,
            "fare_amount": trip.fare_amount,
            "tip_amount": trip.tip_amount,
            "distance_km": trip.distance_km,
            "duration_min": trip.duration_min,
            "passenger_count": trip.passenger_count,
        })    

class Summary(Resource):
    def get(self):
        start = request.args.get("start")
        end = request.args.get("end")

        query = TripModel.query

        # --- Filter by date range ---
        if start:
            try:
                start_date = datetime.strptime(start, "%Y-%m-%d")
                query = query.filter(func.date(TripModel.pickup_datetime) >= start_date)
            except ValueError:
                pass

        if end:
            try:
                end_date = datetime.strptime(end, "%Y-%m-%d")
                query = query.filter(func.date(TripModel.pickup_datetime) <= end_date)
            except ValueError:
                pass

        # --- Aggregated values ---
        agg_result = query.with_entities(
            func.count().label("total_trips"),
            func.avg(TripModel.distance_km).label("avg_distance_km"),
            func.avg(TripModel.duration_min).label("avg_duration_min"),
            func.sum(func.coalesce(TripModel.fare_amount, 0) + func.coalesce(TripModel.tip_amount, 0)).label("total_revenue")
        ).first()

        # --- Trips per hour ---
        trips_by_hour = (
            query.with_entities(
                func.strftime('%H', TripModel.pickup_datetime).label("hour"),
                func.count().label("count")
            )
            .group_by("hour")
            .order_by("hour")
            .all()
        )

        trips_per_hour = [{"hour": row.hour, "count": row.count} for row in trips_by_hour]

        return jsonify({
            "total_trips": int(agg_result.total_trips or 0),
            "avg_distance_km": float(agg_result.avg_distance_km or 0),
            "avg_duration_min": float(agg_result.avg_duration_min or 0),
            "total_revenue": float(agg_result.total_revenue or 0),
            "trips_per_hour": trips_per_hour
        })


api.add_resource(Trip, '/api/trips')
api.add_resource(TripDetail, '/api/trip/<string:trip_id>')
api.add_resource(Summary, '/api/summary')


if __name__ == '__main__':
    app.run(debug=True)
