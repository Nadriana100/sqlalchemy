## Step 2 - Climate App
from flask import Flask, jsonify

from matplotlib import style
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

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
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end>"
    )

### Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
### Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def monthprecp():

    session = Session(engine)

    precp = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date <= 2017,8,23).filter(Measurement.date >= 2016,8,23).all()

    session.close()

    results_dic = []
    for date, prcp in precp:
        months_precp = {}
        months_precp["date"] = date
        months_precp["prcp"] = prcp
       
    return jsonify(results_dic)   

if __name__ == '__main__':
    app.run(debug=True)


       