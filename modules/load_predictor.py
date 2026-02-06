import statistics

def predict_load(flight, passenger_rules):
    p = flight["passenger"]
    hist = p.get("historical_load_pct") or []
    cap = p["capacity"]
    booked = p["booked"]

    if not hist:
        predicted_pct = (booked / cap) * 100 if cap else 0
    else:
        w = passenger_rules.get("moving_avg_window", 7)
        recent = hist[-min(w, len(hist)):]
        predicted_pct = statistics.mean(recent)

    predicted_count = int((predicted_pct / 100) * cap)

    over_pct = passenger_rules["overbooking_threshold_pct"]
    overbook = booked > int(cap * (1 + over_pct / 100))

    under_util = predicted_pct < passenger_rules["under_utilization_pct"]

    return {
        "predicted_passengers": predicted_count,
        "predicted_load_pct": predicted_pct,
        "overbooking_risk": overbook,
        "under_utilized": under_util
    }
