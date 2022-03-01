## Step 2 - Climate App
from flask import Flask, jsonify

import sqlalchemy
#from matplotlib import style
import numpy as np
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tablesn
Base.prepare(engine, reflect=True)

Base.classes.keys()
Base.metadata.tables

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
#################################################
app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""   
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start/end"
    )

### Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
### Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def monthprecp():

    session = Session(engine)

    precp = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date <= "2017-8-23").filter(Measurement.date >= "2016-8-23").all()

    session.close()

    results_dic = {}
    for date, prcp in precp:
        results_dic[date] = prcp
          
    return (results_dic)

####### QUERY 2 ####### JSON list of stations from the dataset  #########
#################/api/v1.0/stations##############

@app.route("/api/v1.0/stations")

def stationlist():       
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    stations_list = list(np.ravel(results))

    return jsonify(stations_list)

      ####### QUERY 3 ####### 
####JSON list of temperature observations (TOBS) for the previous year active station = "USC00519281" for the last year of data #####
##################`/api/v1.0/tobs`##############

@app.route("/api/v1.0/tobs")
    
def tempetarure():

    session = Session(engine)

    t_months=session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date <= "2017-8-23").filter(Measurement.date >= "2016-8-23").all()

    session.close()

    tobslist = list(np.ravel(t_months))
    return jsonify(tobslist)

    ####### QUERY 4 ####### JSON list of the MIN t , the AVG t, and the MAX t for start-end range
    #################`/api/v1.0/start/end` ############## Start Date = '2010-01-01' and End Date = "2017-8-23"

@app.route("/api/v1.0/start/end")
    
def tstart():

    session = Session(engine)

    station_t = [Measurement.date, 
        func.min(Measurement.tobs), 
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)]

    results=session.query(*station_t).filter(Measurement.date <= "2017-8-23").filter(Measurement.date >= "2010-01-01").all()

    session.close()

    startslist = list(np.ravel(results))
    return jsonify(startslist)
    
    


if __name__ == '__main__':
    app.run(debug=True)