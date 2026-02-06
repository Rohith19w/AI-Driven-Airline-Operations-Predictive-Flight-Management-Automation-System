def evaluate_crew(flight, crew_rules):
    pilots = flight["crew"]["pilots"]
    cabin = flight["crew"]["cabin_crew"]

    min_p = crew_rules["min_pilots"]
    min_c = crew_rules["min_cabin_crew"]
    min_rest = crew_rules["min_rest_hours"]
    max_daily = crew_rules["max_daily_hours"]
    flight_hours = crew_rules.get("assumed_flight_hours", 3)

    reasons = []
    ok = True

    if len(pilots) < min_p:
        ok = False
        reasons.append(f"Pilot shortage ({len(pilots)}/{min_p})")

    if len(cabin) < min_c:
        ok = False
        reasons.append(f"Cabin crew shortage ({len(cabin)}/{min_c})")

    for p in pilots:
        if p.get("last_rest", 0) < min_rest:
            ok = False
            reasons.append(f"Pilot {p.get('id')} rest non-compliant ({p.get('last_rest')}h)")

        if p.get("hours_worked", 0) + flight_hours > max_daily:
            ok = False
            reasons.append(f"Pilot {p.get('id')} duty limit risk ({p.get('hours_worked')}h)")

    return ok, reasons
