import csv
from datetime import datetime

def parse_engine_logs(file_path='data/engine_performance.log'):
    engine_data = {}
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            timestamp, fid, acid = parts[0], parts[1], parts[2]
            
            thrust = list(map(float, parts[3].split(':')[1].split(',')))
            vibration = list(map(float, parts[4].split(':')[1].split(',')))
            fuel_burn = float(parts[5].split(':')[1])
            status = parts[6].split(':')[1]
            
            engine_data[fid] = {
                'timestamp': timestamp,
                'aircraft_id': acid,
                'engine_thrust': thrust,
                'engine_vibration': vibration,
                'fuel_burn': fuel_burn,
                'status': status
            }
    return engine_data

def parse_cabin_logs(file_path='data/cabin_pressure.log'):
    cabin_data = {}
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            fid = parts[1]
            
            pressure = float(parts[3].split(':')[1])
            temp = float(parts[4].split(':')[1])
            turbulence = int(parts[5].split(':')[1])
            status = parts[6].split(':')[1]
            
            cabin_data[fid] = {
                'cabin_pressure': pressure,
                'cabin_temp': temp,
                'turbulence': turbulence,
                'status': status
            }
    return cabin_data

def parse_weather_logs(file_path='data/weather_data.log'):
    weather_data = {}
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            fid = parts[1]
            origin, dest = parts[2], parts[3]
            
            crosswind = int(parts[4].split(':')[1])
            visibility = int(parts[5].split(':')[1])
            thunderstorm = parts[6].split(':')[1] == 'YES'
            condition = parts[7].split(':')[1]
            
            weather_data[fid] = {
                'origin': origin,
                'destination': dest,
                'crosswind': crosswind,
                'visibility': visibility,
                'thunderstorm': thunderstorm,
                'condition': condition
            }
    return weather_data

def parse_airspeed_logs(file_path='data/airspeed_altitude.log'):
    airspeed_data = {}
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            fid = parts[1]
            
            airspeed = int(parts[3].split(':')[1])
            altitude = int(parts[4].split(':')[1])
            status = parts[5].split(':')[1]
            
            airspeed_data[fid] = {
                'airspeed': airspeed,
                'altitude': altitude,
                'status': status
            }
    return airspeed_data

def parse_crew_schedule(file_path='data/crew_schedule.csv'):
    crew_data = {}
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fid = row['FlightID']
            pilots = row['PilotIDs'].split(';')
            cabin = row['CabinCrewIDs'].split(';')
            hours = list(map(int, row['HoursWorked'].split(';')))
            rest = list(map(int, row['LastRest'].split(';')))
            available = row['Available'] == 'YES'
            
            crew_data[fid] = {
                'pilots': [{'id': pilots[i], 'hours_worked': hours[i], 'last_rest': rest[i]} 
                          for i in range(len(pilots))],
                'cabin_crew': [{'id': c, 'hours_worked': 4, 'last_rest': 8} for c in cabin],
                'available': available
            }
    return crew_data

def parse_passenger_load(file_path='data/passenger_load.csv'):
    passenger_data = {}
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fid = row['FlightID']
            booked = int(row['Booked'])
            capacity = int(row['Capacity'])
            historical = list(map(int, row['HistoricalLoad'].split(';')))
            
            passenger_data[fid] = {
                'booked': booked,
                'capacity': capacity,
                'historical_load': historical
            }
    return passenger_data

def integrate_flight_data():
    engine = parse_engine_logs()
    cabin = parse_cabin_logs()
    weather = parse_weather_logs()
    airspeed = parse_airspeed_logs()
    crew = parse_crew_schedule()
    passenger = parse_passenger_load()
    
    flights = []
    for fid in engine.keys():
        flight = {
            'flight_id': fid,
            'aircraft_id': engine[fid]['aircraft_id'],
            'timestamp': engine[fid]['timestamp'],
            'metrics': {
                'engine_thrust': engine[fid]['engine_thrust'],
                'engine_vibration': engine[fid]['engine_vibration'],
                'fuel_burn': engine[fid]['fuel_burn'],
                'cabin_pressure': cabin[fid]['cabin_pressure'],
                'cabin_temp': cabin[fid]['cabin_temp'],
                'turbulence': cabin[fid]['turbulence'],
                'airspeed': airspeed[fid]['airspeed'],
                'altitude': airspeed[fid]['altitude']
            },
            'status': {
                'weather': {
                    'crosswind': weather[fid]['crosswind'],
                    'visibility': weather[fid]['visibility'],
                    'thunderstorm': weather[fid]['thunderstorm']
                },
                'operational': {
                    'runway_queue': 20,
                    'boarding_time': 35,
                    'crew_available': crew[fid]['available']
                }
            },
            'passenger': passenger[fid],
            'crew': crew[fid],
            'route': {
                'origin': weather[fid]['origin'],
                'destination': weather[fid]['destination'],
                'alternate': ['HYD', 'CCU']
            }
        }
        flights.append(flight)
    
    return {'flights': flights}
