#Import all the dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from dateutil.parser import parse
from datetime import datetime, timedelta
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=True, connect_args={"check_same_thread": False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################




@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"The list of precipitation data with dates:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"The list of stations and names:<br/>"
        f"/api/v1.0/stations<br/>"
        f"The list of temperture observations from a year from the most active station:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Min. Max. and Avg. tempratures for given start and end date for the most active station:<br/>"
        f"/api/v1.0/start_end<br/>"
        f"i.e. <a href='/api/v1.0/min_max_avg/2012-01-01/2016-12-31' target='_blank'>/api/v1.0/min_max_avg/2012-01-01/2016-12-31</a>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    max_date = dt.date(2017, 8, 23)
    
    days = timedelta(365)

    last_year_date = max_date - days
            

    prcp_data = (session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date <= max_date)\
    .filter(Measurement.date >= last_year_date)\
    .order_by(Measurement.date).all())

    prcp_dict = dict(prcp_data)
        
    return jsonify(prcp_dict)

@app.route('/api/v1.0/stations')
def stations():

    stations_all = session.query(Station.station).all()

    return jsonify(stations_all)

@app.route('/api/v1.0/tobs')
def tobs():
    max_date = dt.date(2017, 8, 23)
    
    days = timedelta(365)

    last_year_date = max_date - days

    most_active_station = session.query(Measurement.date, Measurement.station, Measurement.tobs)\
    .filter(Measurement.date <= max_date)\
    .filter(Measurement.date >= last_year_date)\
    .filter(Measurement.station == "USC00519281").all()

    return jsonify(most_active_station)

@app.route('/api/v1.0/start_end') 
def start_end():
    max_date = dt.date(2017, 8, 23)
    
    days = timedelta(365)

    last_year_date = max_date - days


    temps = session.query(Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Measurement.date <= max_date)\
    .filter(Measurement.date >= last_year_date)\
    .filter(Measurement.station == "USC00519281").all()

    return jsonify(temps)

if __name__ == "__main__":

    app.run(debug=True)

session.close()