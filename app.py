#import dependencies
import numpy as np
import panda as pd
import datetime at dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlaclhemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask

engine=create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect the existing database into a new model
Base=automap_base()

#reflect the tables
Base.prepare(engine, reflect=True)

#Put the references in table
Measurement=Base.classes.measurement
Station=Base.classes.Station

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
           f"/api/v1.0/yyyy-mm-dd<br/>"
           f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

#defing the app when the user hits the precipitation route
@app.route("/api/v1.0/preciptiation")
def precipitation:
    session=Session.bind_engine

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
def station:
    session=Session.bind_engine

    station=session.query(Station.station).all()

    session.close()

    session_list=[r[0] for r in stations]

    return jsonify(station_list)

#defining the app when the user hits the tobs route
@app.route("/api/v1.0/tobs")
def tobs:
    session=Session(engine)

    last_day=dt.date(int(max(session.query(Measurement.date).all())[0][:4]),
                 int(max(session.query(Measurement.date).all())[0][5:7]),
                 int(max(session.query(Measurement.date).all()[0][8:]))
    last_year=last_day-dt.timedelta(dasy=365)

    temps=session.query(Measurement.tobs).filter(Measure.station=="USC00519281").\
                                      filter(Measurement.date>=last_year.strftime(%Y-%m-%d)).\
                                      order_by(Measurement.date).all()

    session.close()

    return jsonify(temps)

#defining the app when the user hits start date