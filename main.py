import json
import os
from modules.log_processor import integrate_flight_data
from modules.health_monitor import check_health
from modules.delay_predictor import predict_delay
from modules.crew_optimizer import optimize_crew
from modules.load_predictor import predict_load
from modules.dashboard import display_dashboard
from modules.reporter import generate_report

def main():
    print("Starting Airline Operations System...")
    print("Reading log files...\n")
    
    with open('airline_config.json') as f:
        config = json.load(f)
    
    data = integrate_flight_data()
    flights = data['flights']
    
    print(f"Loaded {len(flights)} flights from logs")
    
    crew_pool = {
        "pilots": [{"id": f"P{i}", "hours_worked": i*2, "last_rest": 8, "available": True} 
                   for i in range(1,20)],
        "cabin_crew": [{"id": f"C{i}", "hours_worked": i, "last_rest": 6, "available": True} 
                       for i in range(1,30)]
    }
    
    delays = []
    alerts = []
    assignments = {}
    shortages = []
    predictions = {}
    loads = []
    
    for f in flights:
        flight_alerts = check_health(f, config['thresholds'])
        alerts.extend(flight_alerts)
        
        d, r = predict_delay(f, config['thresholds'])
        delays.append((d, r, f['flight_id']))
        
        a, short, sugg = optimize_crew(f, crew_pool, config['crew_rules'])
        assignments[f['flight_id']] = a
        if short:
            shortages.append((f['flight_id'], sugg))
        
        p, over, under = predict_load(f, config['passenger_rules'])
        load_factor = (p / f['passenger']['capacity']) * 100
        predictions[f['flight_id']] = {
            'count': p,
            'load_factor': load_factor,
            'overbooking': over,
            'under_util': under
        }
        loads.append(load_factor)
    
    display_dashboard(flights, delays, alerts, shortages, loads)
    generate_report(flights, delays, alerts, assignments, predictions, config)

if __name__ == "__main__":
    os.makedirs('logs', exist_ok=True)
    os.makedirs('output/reports', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    main()
