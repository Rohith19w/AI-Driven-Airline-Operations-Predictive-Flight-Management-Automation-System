import csv
import os

def validate_csv(filepath, required_headers):
    if not os.path.exists(filepath):
        print(f"❌ Missing: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = [h.strip() for h in reader.fieldnames]
        
        missing = [h for h in required_headers if h not in headers]
        extra = [h for h in headers if h not in required_headers]
        
        if missing:
            print(f"❌ {filepath}: Missing headers: {missing}")
            return False
        if extra:
            print(f"⚠️  {filepath}: Extra headers: {extra}")
        
        row_count = sum(1 for _ in reader)
        print(f"✓ {filepath}: {row_count} rows, headers OK")
        return True

files_to_check = {
    "data/crew_schedule.csv": ["FlightID", "PilotIDs", "CabinCrewIDs", "PilotHoursWorked", "PilotLastRestHours", "CrewAvailable"],
    "data/passenger_load.csv": ["FlightID", "Booked", "Capacity", "HistoricalLoadPct"],
    "data/operational_status.csv": ["FlightID", "RunwayQueueMin", "BoardingTimeMin"]
}

print("Validating CSV files...\n")
all_valid = True
for filepath, headers in files_to_check.items():
    if not validate_csv(filepath, headers):
        all_valid = False
    print()

if all_valid:
    print("✓ All CSV files are valid!")
else:
    print("❌ Some CSV files have issues. Please fix them.")
