import csv
from datetime import datetime

def _parse_kv(token):
    k, v = token.split(":", 1)
    return k.strip(), v.strip()

def _parse_dt(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

def parse_engine_logs(path="data/engine_performance.log"):
    out = {}
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            parts = line.split("|")
            ts = _parse_dt(parts[0])
            fid = parts[1].strip()
            aid = parts[2].strip()

            k1, v1 = _parse_kv(parts[3])
            k2, v2 = _parse_kv(parts[4])
            k3, v3 = _parse_kv(parts[5])
            k4, v4 = _parse_kv(parts[6])

            thrust = [float(x) for x in v1.split(",")] if v1 else []
            vibration = [float(x) for x in v2.split(",")] if v2 else []
            fuel_burn = float(v3)
            status = v4

            out[fid] = {
                "timestamp": ts,
                "flight_id": fid,
                "aircraft_id": aid,
                "engine_thrust": thrust,
                "engine_vibration": vibration,
                "fuel_burn": fuel_burn,
                "engine_status": status
            }
    return out

def parse_cabin_logs(path="data/cabin_pressure.log"):
    series = {}
    meta = {}

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            parts = line.split("|")
            ts = _parse_dt(parts[0])
            fid = parts[1].strip()
            aid = parts[2].strip()

            _, p = _parse_kv(parts[3])
            _, t = _parse_kv(parts[4])
            _, turb = _parse_kv(parts[5])
            _, status = _parse_kv(parts[6])

            pressure = float(p)
            temp = float(t)
            turbulence = int(turb)

            series.setdefault(fid, []).append({"ts": ts, "pressure": pressure})
            meta[fid] = {
                "flight_id": fid,
                "aircraft_id": aid,
                "cabin_pressure": pressure,
                "cabin_temp": temp,
                "turbulence": turbulence,
                "cabin_status": status,
                "timestamp": ts
            }

    for fid in series:
        series[fid].sort(key=lambda x: x["ts"])
        pressures = [x["pressure"] for x in series[fid]]
        meta[fid]["pressure_series"] = pressures
        if len(pressures) >= 2:
            meta[fid]["prev_cabin_pressure"] = pressures[-2]
        else:
            meta[fid]["prev_cabin_pressure"] = None

    return meta

def parse_weather_logs(path="data/weather_data.log"):
    out = {}
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            parts = line.split("|")
            ts = _parse_dt(parts[0])
            fid = parts[1].strip()
            origin = parts[2].strip()
            dest = parts[3].strip()

            _, cw = _parse_kv(parts[4])
            _, vis = _parse_kv(parts[5])
            _, tsf = _parse_kv(parts[6])
            _, cond = _parse_kv(parts[7])

            out[fid] = {
                "timestamp": ts,
                "flight_id": fid,
                "origin": origin,
                "destination": dest,
                "crosswind": int(cw),
                "visibility": int(vis),
                "thunderstorm": (tsf.upper() == "YES"),
                "condition": cond
            }
    return out

def parse_airspeed_altitude_logs(path="data/airspeed_altitude.log"):
    out = {}
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            parts = line.split("|")
            ts = _parse_dt(parts[0])
            fid = parts[1].strip()
            aid = parts[2].strip()

            _, spd = _parse_kv(parts[3])
            _, alt = _parse_kv(parts[4])
            _, status = _parse_kv(parts[5])

            out[fid] = {
                "timestamp": ts,
                "flight_id": fid,
                "aircraft_id": aid,
                "airspeed": int(spd),
                "altitude": int(alt),
                "airspeed_status": status
            }
    return out

def parse_operational_status(path="data/operational_status.csv"):
    out = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fid = row["FlightID"].strip()
            out[fid] = {
                "runway_queue": int(row["RunwayQueueMin"]),
                "boarding_time": int(row["BoardingTimeMin"])
            }
    return out

def parse_crew_schedule(file_path='data/crew_schedule.csv'):
    crew_data = {}
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                fid = row.get('FlightID')
                if not fid:
                    continue
                
                pilots = row.get('PilotIDs', '').split(';') if row.get('PilotIDs') else []
                cabin = row.get('CabinCrewIDs', '').split(';') if row.get('CabinCrewIDs') else []
                
                hours_str = row.get('HoursWorked', '')
                rest_str = row.get('LastRest', '')
                
                hours = [int(x) for x in hours_str.split(';')] if hours_str else []
                rest = [int(x) for x in rest_str.split(';')] if rest_str else []
                
                crew_data[fid] = {
                    'pilots': [{'id': p, 'hours_worked': h, 'last_rest': r} for p, h, r in zip(pilots, hours, rest)],
                    'cabin_crew': [{'id': c} for c in cabin],
                    'available': row.get('Available', 'NO').upper() == 'YES'
                }
    except FileNotFoundError:
        print(f"Warning: {file_path} not found.")
    except KeyError as e:
        print(f"Error reading CSV header in crew schedule: Missing column {e}")
        
    return crew_data

def parse_passenger_load(path="data/passenger_load.csv"):
    out = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fid = row["FlightID"].strip()
            hist = [int(x) for x in row["HistoricalLoadPct"].split(";") if x.strip()]
            out[fid] = {
                "flight_id": fid,
                "booked": int(row["Booked"]),
                "capacity": int(row["Capacity"]),
                "historical_load_pct": hist
            }
    return out

def integrate_flight_data(
    engine_path="data/engine_performance.log",
    cabin_path="data/cabin_pressure.log",
    weather_path="data/weather_data.log",
    airspeed_path="data/airspeed_altitude.log",
    ops_path="data/operational_status.csv",
    crew_path="data/crew_schedule.csv",
    pax_path="data/passenger_load.csv"
):
    engine = parse_engine_logs(engine_path)
    cabin = parse_cabin_logs(cabin_path)
    weather = parse_weather_logs(weather_path)
    airspeed = parse_airspeed_altitude_logs(airspeed_path)
    ops = parse_operational_status(ops_path)
    crew = parse_crew_schedule(crew_path)
    pax = parse_passenger_load(pax_path)

    flight_ids = set()
    for d in (engine, cabin, weather, airspeed, ops, crew, pax):
        flight_ids.update(d.keys())

    flights = []
    missing = []

    for fid in sorted(flight_ids):
        if fid not in engine or fid not in cabin or fid not in weather or fid not in airspeed or fid not in ops or fid not in crew or fid not in pax:
            missing.append(fid)
            continue

        flights.append({
            "flight_id": fid,
            "aircraft_id": engine[fid]["aircraft_id"],
            "timestamp": engine[fid]["timestamp"].isoformat(sep=" "),
            "metrics": {
                "engine_thrust": engine[fid]["engine_thrust"],
                "engine_vibration": engine[fid]["engine_vibration"],
                "fuel_burn": engine[fid]["fuel_burn"],
                "cabin_pressure": cabin[fid]["cabin_pressure"],
                "prev_cabin_pressure": cabin[fid].get("prev_cabin_pressure"),
                "cabin_temp": cabin[fid]["cabin_temp"],
                "turbulence": cabin[fid]["turbulence"],
                "airspeed": airspeed[fid]["airspeed"],
                "altitude": airspeed[fid]["altitude"]
            },
            "status": {
                "codes": {
                    "engine": engine[fid]["engine_status"],
                    "cabin": cabin[fid]["cabin_status"],
                    "airspeed": airspeed[fid]["airspeed_status"]
                },
                "weather": {
                    "crosswind": weather[fid]["crosswind"],
                    "visibility": weather[fid]["visibility"],
                    "thunderstorm": weather[fid]["thunderstorm"],
                    "condition": weather[fid]["condition"]
                },
                "operational": {
                    "runway_queue": ops[fid]["runway_queue"],
                    "boarding_time": ops[fid]["boarding_time"],
                    "crew_available": crew[fid]["crew_available"]
                }
            },
            "passenger": {
                "booked": pax[fid]["booked"],
                "capacity": pax[fid]["capacity"],
                "historical_load_pct": pax[fid]["historical_load_pct"]
            },
            "crew": {
                "pilots": crew[fid]["pilots"],
                "cabin_crew": crew[fid]["cabin_crew"]
            },
            "route": {
                "origin": weather[fid]["origin"],
                "destination": weather[fid]["destination"],
                "alternate": ["HYD", "CCU", "AMD"]
            }
        })

    return {"flights": flights, "missing_flights": missing}
