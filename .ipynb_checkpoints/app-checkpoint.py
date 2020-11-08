{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Set up dependencies\n",
    "from flask import Flask , jsonify\n",
    "import sqlalchemy\n",
    "from sqlalchemy import create_engine, func\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "import datetime as dt \n",
    "import pandas as pd\n",
    "# from sqlalchemy.orm import scoped_session, sessionmaker"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## API SQLite Connection & Landing Page"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "engine = create_engine(\"sqlite:///Resources/hawaii.sqlite\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "# reflect an existing database into a new model\n",
    "Base = automap_base()\n",
    "# reflect the tables\n",
    "Base.prepare(engine, reflect=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Save references to each table\n",
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create our session (link) from Python to the DB\n",
    "session = Session(engine)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "datetime.date(2016, 8, 23)"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Design a query to retrieve the last 12 months of precipitation data and plot the results\n",
    "latest_date = pd.to_datetime(session.query(Measurement.date).order_by(Measurement.date.desc()).first())\n",
    "\n",
    "year=(latest_date.year)\n",
    "#year\n",
    "month=latest_date.month\n",
    "#month\n",
    "day=latest_date.day\n",
    "#day\n",
    "\n",
    "# Calculate the date 1 year ago from the last data point in the database\n",
    "date_oneYearAgo= dt.date(year[0],month[0], day[0]) - dt.timedelta(days=365)\n",
    "\n",
    "date_oneYearAgo"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "# date_oneYearAgo\n",
    "\n",
    "# Perform a query to retrieve the data and precipitation scores\n",
    "# prcp_scores = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date.desc()).all()\n",
    "# prcp_scores\n",
    "# date_prcp\n",
    "date_prcp = session.query(Measurement.date, Measurement.prcp).\\\n",
    "    filter(Measurement.date >= date_oneYearAgo).\\\n",
    "    order_by(Measurement.date).all()\n",
    "# date_prcp"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## API Static Routes"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Flask Setup\n",
    "app = Flask(__name__)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "ename": "AssertionError",
     "evalue": "View function mapping is overwriting an existing endpoint function: welcome",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mAssertionError\u001b[0m                            Traceback (most recent call last)",
      "\u001b[1;32m<ipython-input-19-86734f16219d>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m()\u001b[0m\n\u001b[1;32m----> 1\u001b[1;33m \u001b[1;33m@\u001b[0m\u001b[0mapp\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mroute\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34m\"/\"\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      2\u001b[0m \u001b[1;32mdef\u001b[0m \u001b[0mwelcome\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      3\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      4\u001b[0m     return (\n\u001b[0;32m      5\u001b[0m         \u001b[1;34mf\"Available Routes:<br/>\"\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32mC:\\Users\\Mengyin\\anaconda3\\envs\\PythonData\\lib\\site-packages\\flask\\app.py\u001b[0m in \u001b[0;36mdecorator\u001b[1;34m(f)\u001b[0m\n\u001b[0;32m   1313\u001b[0m         \u001b[1;32mdef\u001b[0m \u001b[0mdecorator\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mf\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m   1314\u001b[0m             \u001b[0mendpoint\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0moptions\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mpop\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34m\"endpoint\"\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;32mNone\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m-> 1315\u001b[1;33m             \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0madd_url_rule\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mrule\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mendpoint\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mf\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;33m**\u001b[0m\u001b[0moptions\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m   1316\u001b[0m             \u001b[1;32mreturn\u001b[0m \u001b[0mf\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m   1317\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32mC:\\Users\\Mengyin\\anaconda3\\envs\\PythonData\\lib\\site-packages\\flask\\app.py\u001b[0m in \u001b[0;36mwrapper_func\u001b[1;34m(self, *args, **kwargs)\u001b[0m\n\u001b[0;32m     96\u001b[0m                 \u001b[1;34m\"before the application starts serving requests.\"\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     97\u001b[0m             )\n\u001b[1;32m---> 98\u001b[1;33m         \u001b[1;32mreturn\u001b[0m \u001b[0mf\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;33m*\u001b[0m\u001b[0margs\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;33m**\u001b[0m\u001b[0mkwargs\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m     99\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    100\u001b[0m     \u001b[1;32mreturn\u001b[0m \u001b[0mupdate_wrapper\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mwrapper_func\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mf\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32mC:\\Users\\Mengyin\\anaconda3\\envs\\PythonData\\lib\\site-packages\\flask\\app.py\u001b[0m in \u001b[0;36madd_url_rule\u001b[1;34m(self, rule, endpoint, view_func, provide_automatic_options, **options)\u001b[0m\n\u001b[0;32m   1282\u001b[0m                 raise AssertionError(\n\u001b[0;32m   1283\u001b[0m                     \u001b[1;34m\"View function mapping is overwriting an \"\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m-> 1284\u001b[1;33m                     \u001b[1;34m\"existing endpoint function: %s\"\u001b[0m \u001b[1;33m%\u001b[0m \u001b[0mendpoint\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m   1285\u001b[0m                 )\n\u001b[0;32m   1286\u001b[0m             \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mview_functions\u001b[0m\u001b[1;33m[\u001b[0m\u001b[0mendpoint\u001b[0m\u001b[1;33m]\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mview_func\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;31mAssertionError\u001b[0m: View function mapping is overwriting an existing endpoint function: welcome"
     ]
    }
   ],
   "source": [
    "@app.route(\"/\")\n",
    "def welcome():\n",
    "\n",
    "    return (\n",
    "        f\"Available Routes:<br/>\"\n",
    "        f\"The precipitation information from the last year's available data :<br/>\"\n",
    "        f\"/api/v1.0/precipitation<br/>\"\n",
    "        f\"List of stations from the dataset:<br/>\"\n",
    "        f\"/api/v1.0/stations<br/>\"\n",
    "        f\"List of Temperature Observations (tobs) of the most active station for the previous year:<br/>\"\n",
    "        f\"/api/v1.0/tobs<br/>\"\n",
    "        f\"List of the minimum temperature, the average temperature, and the max temperature for a given start(i.e.2017-1-1):<br/>\"\n",
    "        f\"/api/v1.0/<start><br/>\"\n",
    "        f\"List of the minimum temperature, the average temperature, and the max temperature for a given start and end(i.e.2017-01-01/2017-01-07):<br/>\"\n",
    "        f\"/api/v1.0/<start>/<end><br/>\"\n",
    "    )\n",
    "\n",
    "\n",
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "def precipitation():\n",
    "\n",
    "    date_prcp = session.query(Measurement.date, Measurement.prcp).\\\n",
    "    filter(Measurement.date >= date_oneYearAgo).\\\n",
    "    order_by(Measurement.date).all()\n",
    "\n",
    "    precipitation_data = dict(date_prcp)\n",
    "\n",
    "    return jsonify({'Data':precipitation_data})\n",
    "\n",
    "@app.route(\"/api/v1.0/stations\")\n",
    "def stations():\n",
    "    stations = session.query(Station).all()\n",
    "    stations_list = list()\n",
    "    \n",
    "    for station in stations:\n",
    "        stations_dict = dict()\n",
    "        stations_dict['Station'] = station.station\n",
    "        stations_dict[\"Station Name\"] = station.name\n",
    "        stations_dict[\"Latitude\"] = station.latitude\n",
    "        stations_dict[\"Longitude\"] = station.longitude\n",
    "        stations_dict[\"Elevation\"] = station.elevation\n",
    "        stations_list.append(stations_dict)\n",
    "\n",
    "    return jsonify ({'Data':stations_list})"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## API Dynamic Route"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/tobs\")\n",
    "def tobs():\n",
    "\n",
    "    latest_year_tobs = session.query(\n",
    "        Measurement.tobs,\n",
    "        Measurement.date,\n",
    "        Measurement.station).\\\n",
    "    filter(Measurement.date > date_oneYearAgo).all()\n",
    "\n",
    "    temp_list = list()\n",
    "    for data in latest_year_tobs:\n",
    "        temp_dict = dict()\n",
    "        temp_dict['Station'] = data.station\n",
    "        temp_dict['Date'] = data.date\n",
    "        temp_dict['Temp'] = data.tobs\n",
    "        temp_list.append(temp_dict)\n",
    "\n",
    "    return jsonify ({'Data':temp_list})\n",
    "\n",
    "@app.route(\"/api/v1.0/<start>\")\n",
    "def start_temp(start=None):\n",
    "\n",
    "\tstart_temps = session.query(\n",
    "\t\tfunc.min(Measurement.tobs), \n",
    "\t\tfunc.avg(Measurement.tobs),\n",
    "\t\tfunc.max(Measurement.tobs)\n",
    "\t).filter(\n",
    "\t\tMeasurement.date >= start\n",
    "\t).all()\n",
    "\n",
    "\n",
    "\tstart_list = list()\n",
    "\tfor tmin, tavg, tmax in start_temps:\n",
    "\t\tstart_dict = {}\n",
    "\t\tstart_dict[\"Min Temp\"] = tmin\n",
    "\t\tstart_dict[\"Max Temp\"] = tavg\n",
    "\t\tstart_dict[\"Avg Temp\"] = tmax\n",
    "\t\tstart_list.append(start_dict)\n",
    "\n",
    "\treturn jsonify ({'Data':start_list})\n",
    "\n",
    "\n",
    "\n",
    "@app.route(\"/api/v1.0/<start>/<end>\")\n",
    "def calc_temps(start=None,end=None):\n",
    "    temps = session.query(\n",
    "        func.min(Measurement.tobs),\n",
    "        func.avg(Measurement.tobs),\n",
    "        func.max(Measurement.tobs)\n",
    "    ).filter(\n",
    "    \tMeasurement.date >= start,\n",
    "    \tMeasurement.date <= end\n",
    "    ).all()\n",
    "\n",
    "    temp_list = list()\n",
    "    for tmin, tavg, tmax in temps:\n",
    "    \ttemp_dict = dict()\n",
    "    \ttemp_dict[\"Min Temp\"] = tmin\n",
    "    \ttemp_dict[\"Avg Temo\"] = tavg\n",
    "    \ttemp_dict[\"Max Temp\"] = tmax\n",
    "    \ttemp_list.append(temp_dict)\n",
    "\n",
    "    return jsonify ({'Data':temp_list})"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "   WARNING: This is a development server. Do not use it in a production deployment.\n",
      "   Use a production WSGI server instead.\n",
      " * Debug mode: on\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Restarting with stat\n"
     ]
    },
    {
     "ename": "SystemExit",
     "evalue": "1",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[1;31mSystemExit\u001b[0m\u001b[1;31m:\u001b[0m 1\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Mengyin\\anaconda3\\envs\\PythonData\\lib\\site-packages\\IPython\\core\\interactiveshell.py:2886: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.\n",
      "  warn(\"To exit: use 'exit', 'quit', or Ctrl-D.\", stacklevel=1)\n"
     ]
    }
   ],
   "source": [
    "if __name__ == '__main__':\n",
    "    app.run(debug=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernel_info": {
   "name": "python3"
  },
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.10"
  },
  "nteract": {
   "version": "0.12.3"
  },
  "varInspector": {
   "cols": {
    "lenName": 16,
    "lenType": 16,
    "lenVar": 40
   },
   "kernels_config": {
    "python": {
     "delete_cmd_postfix": "",
     "delete_cmd_prefix": "del ",
     "library": "var_list.py",
     "varRefreshCmd": "print(var_dic_list())"
    },
    "r": {
     "delete_cmd_postfix": ") ",
     "delete_cmd_prefix": "rm(",
     "library": "var_list.r",
     "varRefreshCmd": "cat(var_dic_list()) "
    }
   },
   "types_to_exclude": [
    "module",
    "function",
    "builtin_function_or_method",
    "instance",
    "_Feature"
   ],
   "window_display": false
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
