# Climate App
from flask import Flask , jsonify
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt 
import pandas as pd
from sqlalchemy.orm import scoped_session, sessionmaker
#############################################
# API SQLite Connection & Landing Page
#############################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite",echo=False)

Base = automap_base()

Base.prepare(engine, reflect=True)

# Tables: Measurement and Station
Measurement = Base.classes.measurement
Station = Base.classes.station


sess=scoped_session(sessionmaker(bind=engine))

latest_date = pd.to_datetime(sess.query(Measurement.date).order_by(Measurement.date.desc()).first())

year = (latest_date.year)
month = (latest_date.month)
day = (latest_date.day)

# calculate the date one year ago from the latest date of the data set
date_oneYearAgo = dt.date(year[0], month[0], day[0]) - dt.timedelta(days=365)

############################################
# Flask Setup
############################################

app = Flask(__name__)

#####################################################
# Welcome page : List all routes that are available
#####################################################

@app.route("/")
def welcome():

    return (
        f"Available Routes:<br/>"
        f"Precipitation observations from the last year of the dataset:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"List of stations from the dataset:<br/>"
        f"/api/v1.0/stations<br/>"
        f"List of Temperature Observations (tobs) for the most active statiion of the last year:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"List of the minimum temperature, the average temperature, and the max temperature for a given start date, enter as yyyy-mm-dd:<br/>"
        f"/api/v1.0/<start><br/>"
        f"List of the minimum temperature, the average temperature, and the max temperature for a given start and end date, enter as yyyy-mm-dd/yyyy-mm-dd:<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

############################################
# API Static Routes
############################################

@app.route("/api/v1.0/precipitation")
def precipitation():
	
	latest_year_data = sess.query(Measurement.date,Measurement.prcp).filter(Measurement.date > date_oneYearAgo).order_by(Measurement.date).all()

	prcp_data = dict(latest_year_data)

	return jsonify({'Data':prcp_data})

@app.route("/api/v1.0/stations")
def stations():
	stations = sess.query(Station).all()
	stations_list = list()
	for station in stations:
		stations_dict = dict()
		stations_dict['Station'] = station.station
		stations_dict["Station Name"] = station.name
		stations_dict["Latitude"] = station.latitude
		stations_dict["Longitude"] = station.longitude
		stations_dict["Elevation"] = station.elevation
		stations_list.append(stations_dict)

	return jsonify ({'Data':stations_list})

@app.route("/api/v1.0/tobs")
def tobs():

	latest_year_tobs = sess.query(Measurement.tobs,Measurement.date,Measurement.station).filter(Measurement.date > date_oneYearAgo).filter(Measurement.station == "USC00519281").all()

	temp_list = list()
	for data in latest_year_tobs:
		temp_dict = dict()
		temp_dict['Station'] = data.station
		temp_dict['Date'] = data.date
		temp_dict['Temp'] = data.tobs
		temp_list.append(temp_dict)

	return jsonify ({'Data':temp_list})

##########################################################
# API Dynamic Routes
###########################################################

# Route accepts the start date as a parameter from the URL

@app.route("/api/v1.0/<startDate>")
def start_temp(startDate=None):

	start_temps = sess.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= startDate).all()

	startDate_list = list()
	for tmin, tavg, tmax in start_temps:
		start_dict = {}
		start_dict["Min Temp"] = tmin
		start_dict["Avg Temp"] = tavg
		start_dict["Max Temp"] = tmax
		startDate_list.append(start_dict)

	return jsonify ({'Data':startDate_list})

# Route accepts the start and end dates as a parameter from the URL

@app.route("/api/v1.0/<startDate>/<endDate>")
def calc_temps(startDate=None,endDate=None):
    temps = sess.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= startDate,Measurement.date <= endDate).all()

    temp_list = list()
    for tmin, tavg, tmax in temps:
    	temp_dict = dict()
    	temp_dict["Min Temp"] = tmin
    	temp_dict["Avg Temo"] = tavg
    	temp_dict["Max Temp"] = tmax
    	temp_list.append(temp_dict)

    return jsonify ({'Data':temp_list})
 

if __name__ == '__main__':
    app.run(debug=True)