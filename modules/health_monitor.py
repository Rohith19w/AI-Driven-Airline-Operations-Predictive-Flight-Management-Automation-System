
import logging

_health_logger = logging.getLogger("aircraft_health")
_critical_logger = logging.getLogger("critical_flights")

def setup_health_loggers():
    _health_logger.setLevel(logging.INFO)
    _critical_logger.setLevel(logging.CRITICAL)

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    health_handler = logging.FileHandler("logs/aircraft_health_alerts.log", encoding="utf-8")
    health_handler.setFormatter(fmt)
    health_handler.setLevel(logging.INFO)

    critical_handler = logging.FileHandler("logs/critical_flight_alerts.log", encoding="utf-8")
    critical_handler.setFormatter(fmt)
    critical_handler.setLevel(logging.CRITICAL)

    if not _health_logger.handlers:
        _health_logger.addHandler(health_handler)

    if not _critical_logger.handlers:
        _critical_logger.addHandler(critical_handler)

def check_health(flight, thresholds):
    alerts = []
    m = flight["metrics"]
    fid = flight["flight_id"]

    vib = m.get("engine_vibration") or []
    if any(v > thresholds["engine_vibration"] for v in vib):
        msg = f"{fid} | High engine vibration {vib}"
        _critical_logger.critical(msg)
        alerts.append(("CRITICAL", msg))

    turb = m.get("turbulence")
    if turb is not None and turb >= thresholds["turbulence_severe"]:
        msg = f"{fid} | Severe turbulence {turb}"
        _critical_logger.critical(msg)
        alerts.append(("CRITICAL", msg))

    cabin_temp = m.get("cabin_temp")
    if cabin_temp is not None and cabin_temp > thresholds["cabin_temp_high"]:
        msg = f"{fid} | High cabin temperature {cabin_temp}C"
        _health_logger.warning(msg)
        alerts.append(("WARN", msg))

    fuel_burn = m.get("fuel_burn")
    base = thresholds.get("fuel_burn_baseline", 2200)
    if fuel_burn is not None and base:
        dev = abs((fuel_burn - base) / base) * 100
        if dev > thresholds["fuel_burn_deviation"]:
            msg = f"{fid} | Abnormal fuel burn {dev:.1f}%"
            _health_logger.warning(msg)
            alerts.append(("WARN", msg))

    return alerts
