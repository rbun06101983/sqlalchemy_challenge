#import dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine=create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect the existing database into a new model
Base=automap_base()

#reflect the tables
Base.prepare(engine, reflect=True)

#Put the references in table
Measurement=Base.classes.measurement
Station=Base.classes.station

#Creating the app
app=Flask(__name__)

#defining the app our when the user hits the index route
@app.route("/")
def home():
    return(f"Hawaii Weather Report Data<br/>"
           f"available routes:<br/>"
           f"/api/v1.0/precipitation<br/>"
           f"/api/v1.0/stations<br/>"
           f"/api/v1.0/tobs<br/>"
           f"/api/v1.0/start<br/>"
           f"/api/v1.0/start/end<br/>"
    )

#defing the app when the user hits the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(bind=engine)

    precip=session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    rain=[]

    for (date, precipitation) in precip:
        record_dict={}
        record_dict["date"]=date
        record_dict["rain"]=precipitation
        rain.append(record_dict)
    
    return jsonify(rain)

#defining the app when the user hits the station route
@app.route("/api/v1.0/stations")
def stations():
    session=Session(bind=engine)

    station=session.query(Station.station).all()

    session.close()

    station_list=[r[0] for r in station]

    return jsonify(station_list)

#defining the app when the user hits the tobs route
@app.route("/api/v1.0/tobs")
def temperature():
    session=Session(engine)

    last_day=dt.date(int(max(session.query(Measurement.date).all())[0][:4]),
                 int(max(session.query(Measurement.date).all())[0][5:7]),
                 int(max(session.query(Measurement.date).all())[0][8:]))

    last_year=last_day-dt.timedelta(days=365)

    temps=session.query(Measurement.tobs).filter(Measurement.station=="USC00519281").\
                                      filter(Measurement.date>=last_year.strftime("%Y-%m-%d")).\
                                      order_by(Measurement.date).all()

    session.close()

    return jsonify(temps)

#defining the app when the user hits start date
@app.route("/api/v1.0/<start>")
def weather_report(start=None):
    session=Session(engine)

    results= session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                                  filter(Measurement.date >=start).all()
    
    session.close()

    temp_avg=list(np.ravel(results))

    return jsonify(temp_avg)

#defining the app when the user hits a range date
@app.route("/api/v1.0/<start>/<end>")
def range_weather_report(start=None, end=None):
    session=Session(engine)

    results= session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                                  filter(Measurement.date >=start).\
                                  filter(Measurement.date <=end).all()
    
    session.close()

    temp_avg=list(np.ravel(results))

    return jsonify(temp_avg)

if __name__=="__main__":
    app.run(debug=True)