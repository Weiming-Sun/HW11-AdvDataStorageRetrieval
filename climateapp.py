from flask import Flask, jsonify

from sqlalchemy import create_engine
engine = create_engine("sqlite:///hawaii.sqlite")

from sqlalchemy.ext.automap import automap_base
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurements
Station = Base.classes.stations

from sqlalchemy.orm import Session
session = Session(engine)

from sqlalchemy import func

results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > '2016-08-23').\
    filter(Measurement.station == 'USC00519397').all()
    
prcp_dict = {}
for r in results:
    prcp_dict[r.date] = r.prcp

results = session.query(Station.name).all()

stations_list = []
for r in results:
    stations_list.append(r.name)

results = session.query(Measurement.tobs).\
    filter(Measurement.date > '2016-08-23').all()

tobs_list = []
for r in results:
    tobs_list.append(r.tobs)

app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def tempstart(start):
    start_date = str(start)

    session = Session(engine)

    from sqlalchemy import func
    max_temp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.station == 'USC00519397').all()
    min_temp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.station == 'USC00519397').all()
    avg_temp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.station == 'USC00519397').all()

    start_dict = {"From which date": start_date, "max temp": max_temp[0][0], "min temp": min_temp[0][0], "avg": avg_temp[0][0]}

    return jsonify(start_dict)

@app.route("/api/v1.0/<start>/<end>")
def tempstartend(start, end):
    start_date = str(start)
    end_date = str(end)

    session = Session(engine)

    from sqlalchemy import func
    max_temp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        filter(Measurement.station == 'USC00519397').all()
    min_temp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        filter(Measurement.station == 'USC00519397').all()
    avg_temp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        filter(Measurement.station == 'USC00519397').all()

    startend_dict = {"From which date to Which date": start_date+" to "+end_date, "max temp": max_temp[0][0], "min temp": min_temp[0][0], "avg": avg_temp[0][0]}

    return jsonify(startend_dict)

if __name__ == "__main__":
    app.run(debug=True)