from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# Create an instance of the Flask application
app = Flask(__name__)

# Define the homepage route
@app.route("/")
def home():
    """Homepage"""
    return (
        f"Welcome to the Climate Analysis API!<br/><br/>"
        f"Available Routes:<br/><br/>"
        f"Last 12 Months of Precipitation Data: -- /api/v1.0/precipitation<br/>"
        f"Detail of Temperature Observed at Stations: -- /api/v1.0/stations<br/>"
        f"Last 12 Months of Temperature Data: -- /api/v1.0/tobs<br/>"
        f"Temperature Data from Variable Date Ranges: -- /api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

# Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Last 12 Months of Precipitation Data"""
    # Calculate the date 1 year ago from the most recent date
    one_year_ago = dt.date.today() - dt.timedelta(days=365)
    
    # Query the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= one_year_ago)\
        .all()
    
    # Create a dictionary with date as the key and prcp as the value
    precipitation_data = {date: prcp for date, prcp in results}
    
    return jsonify(precipitation_data)

# Define the stations route
@app.route("/api/v1.0/stations")
def stations():
    """List of Stations"""
    # Query all the stations
    results = session.query(Station.station, Station.name).all()
    
    # Create a list of dictionaries with station and name information
    station_list = [{"Station": station, "Name": name} for station, name in results]
    
    return jsonify(station_list)

# Define the temperature observations route
@app.route("/api/v1.0/tobs")
def tobs():
    """Temperature Observations for Most Active Station"""
    # Calculate the date 1 year ago from the most recent date
    one_year_ago = dt.date.today() - dt.timedelta(days=365)
    
    # Query the temperature observations for the most active station
    results = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active_station_id)\
        .filter(Measurement.date >= one_year_ago)\
        .all()
    
    # Create a list of dictionaries with date and tobs information
    tobs_list = [{"Date": date, "Temperature": tobs} for date, tobs in results]
    
    return jsonify(tobs_list)

# Define the start and start-end route
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_stats(start, end=None):
    """Temperature Statistics for a Specified Date Range"""
    # Query the temperature statistics based on the specified date range
    if end:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
            .filter(Measurement.date >= start)\
            .filter(Measurement.date <= end)\
            .all()
    else:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
            .filter(Measurement.date >= start)\
            .all()
    
    # Create a dictionary with the temperature statistics
    temp_stats_dict = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }
    
    return jsonify(temp_stats_dict)

if __name__ == '__main__':
    app.run(debug=True)
