def predict_delay(flight, thresholds):
    delay = 0
    reasons = []

    w = flight["status"]["weather"]
    m = flight["metrics"]
    o = flight["status"]["operational"]

    if w["crosswind"] > thresholds["crosswind_knots"]:
        delay += 30
        reasons.append(f"Crosswind {w['crosswind']} knots")

    if w["thunderstorm"]:
        delay += 60
        reasons.append("Thunderstorm")

    if w["visibility"] < thresholds["visibility_meters"]:
        delay += 25
        reasons.append(f"Low visibility {w['visibility']}m")

    thrusts = m.get("engine_thrust") or []
    if thrusts:
        baseline = thresholds.get("engine_thrust_baseline", 100)
        thrust_dev = max(abs(baseline - t) for t in thrusts)
        if thrust_dev > thresholds["engine_thrust_deviation"]:
            delay += 90
            reasons.append(f"Engine thrust deviation {thrust_dev:.1f}%")

    cabin_pressure = m.get("cabin_pressure")
    prev_pressure = m.get("prev_cabin_pressure")

    if cabin_pressure is not None and cabin_pressure < thresholds["cabin_pressure_min"]:
        delay += 45
        reasons.append("Cabin pressure low")

    if cabin_pressure is not None and prev_pressure is not None:
        drop = prev_pressure - cabin_pressure
        if drop >= thresholds["cabin_pressure_drop"]:
            delay += 45
            reasons.append(f"Sudden pressure drop {drop:.2f}")

    if o["runway_queue"] > thresholds["runway_queue_threshold"]:
        extra = o["runway_queue"] - thresholds["runway_queue_threshold"]
        delay += extra
        reasons.append(f"Runway queue {o['runway_queue']}min")

    if o["boarding_time"] > thresholds["boarding_time_threshold"]:
        extra = o["boarding_time"] - thresholds["boarding_time_threshold"]
        delay += extra * 2
        reasons.append(f"Slow boarding {o['boarding_time']}min")

    if not o["crew_available"]:
        delay += 60
        reasons.append("Crew unavailable")

    return delay, reasons
