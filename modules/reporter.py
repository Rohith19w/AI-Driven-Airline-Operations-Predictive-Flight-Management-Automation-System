import os
from datetime import datetime

def write_daily_report(
    flights,
    delay_results,
    health_alerts,
    crew_issues,
    load_results,
    missing_flights,
    out_dir="output/reports"
):
    os.makedirs(out_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    path = os.path.join(out_dir, f"aviation_report_{date_str}.txt")

    delays_by_id = {d["flight_id"]: d for d in delay_results}
    load_by_id = {l["flight_id"]: l for l in load_results}
    crew_by_id = {c["flight_id"]: c for c in crew_issues}

    with open(path, "w", encoding="utf-8") as f:
        f.write("="*60 + "\n")
        f.write("  DAILY AVIATION OPERATIONS REPORT\n")
        f.write("="*60 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")

        if missing_flights:
            f.write("SKIPPED FLIGHTS (missing data):\n")
            for fid in missing_flights:
                f.write(f"  - {fid}\n")
            f.write("\n")

        f.write("FLIGHT SUMMARY:\n")
        f.write("-"*60 + "\n")
        for fl in flights:
            fid = fl["flight_id"]
            route = f'{fl["route"]["origin"]} → {fl["route"]["destination"]}'
            d = delays_by_id.get(fid, {"delay_min": 0, "reasons": []})
            l = load_by_id.get(fid, {})
            c = crew_by_id.get(fid, {})

            f.write(f"\n{fid} | {fl['aircraft_id']} | {route}\n")
            f.write(f"  Timestamp: {fl['timestamp']}\n")
            f.write(f"  Predicted Delay: {d['delay_min']} min\n")
            
            if d["reasons"]:
                f.write(f"  Reasons: {'; '.join(d['reasons'])}\n")
            
            if l:
                f.write(f"  Load: {l['predicted_load_pct']:.1f}% ({l['predicted_passengers']} pax)\n")
                if l["overbooking_risk"]:
                    f.write("  ⚠ Overbooking risk\n")
                if l["under_utilized"]:
                    f.write("  ⚠ Under-utilized\n")

            if c:
                f.write(f"  Crew: {'; '.join(c['issues'])}\n")

        f.write("\n" + "-"*60 + "\n")
        f.write("HEALTH ALERTS:\n")
        f.write("-"*60 + "\n")
        
        if not health_alerts:
            f.write("No alerts\n")
        else:
            for lvl, msg in health_alerts:
                f.write(f"{lvl}: {msg}\n")

        f.write("\n" + "="*60 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*60 + "\n")

    return path
