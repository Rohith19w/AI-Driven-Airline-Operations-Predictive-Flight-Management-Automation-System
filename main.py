import os
import json

from modules.log_processor import integrate_flight_data
from modules.delay_predictor import predict_delay
from modules.health_monitor import setup_health_loggers, check_health
from modules.crew_optimizer import evaluate_crew
from modules.load_predictor import predict_load
from modules.dashboard import show_dashboard
from modules.reporter import write_daily_report

def main():
    os.makedirs("logs", exist_ok=True)
    os.makedirs("output/reports", exist_ok=True)

    print("Initializing Airline Operations System...")
    
    with open("airline_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    setup_health_loggers()

    print("Reading flight data from logs...")
    data = integrate_flight_data()
    flights = data["flights"]
    missing = data["missing_flights"]

    print(f"Processing {len(flights)} flights...\n")

    delay_results = []
    health_alerts = []
    crew_issues = []
    load_results = []

    for fl in flights:
        delay_min, reasons = predict_delay(fl, config["thresholds"])
        delay_results.append({"flight_id": fl["flight_id"], "delay_min": delay_min, "reasons": reasons})

        health_alerts.extend(check_health(fl, config["thresholds"]))

        ok, issues = evaluate_crew(fl, config["crew_rules"])
        if not ok:
            crew_issues.append({"flight_id": fl["flight_id"], "issues": issues})

        load_pred = predict_load(fl, config["passenger_rules"])
        load_results.append({"flight_id": fl["flight_id"], **load_pred})

    show_dashboard(flights, delay_results, health_alerts, crew_issues, load_results)

    report_path = write_daily_report(
        flights=flights,
        delay_results=delay_results,
        health_alerts=health_alerts,
        crew_issues=crew_issues,
        load_results=load_results,
        missing_flights=missing
    )

    print(f"✓ Report saved: {report_path}")
    print(f"✓ Alerts logged to: logs/")
    
    if missing:
        print(f"\n⚠ Flights skipped: {', '.join(missing)}")

if __name__ == "__main__":
    main()
