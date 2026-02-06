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

    total_flights = len(flights)
    delayed_flights = [d for d in delay_results if d["delay_min"] > 0]
    on_time_flights = total_flights - len(delayed_flights)
    total_delay_time = sum(d["delay_min"] for d in delay_results)
    avg_load = sum(l["predicted_load_pct"] for l in load_results) / len(load_results) if load_results else 0

    critical_alerts = [a for a in health_alerts if a[0] == "CRITICAL"]
    warning_alerts = [a for a in health_alerts if a[0] == "WARN"]

    with open(path, "w", encoding="utf-8") as f:
        f.write("╔" + "═"*88 + "╗\n")
        f.write("║" + " "*25 + "DAILY AVIATION OPERATIONS REPORT" + " "*31 + "║\n")
        f.write("╚" + "═"*88 + "╝\n\n")
        
        f.write(f"Report Date: {datetime.now().strftime('%A, %B %d, %Y')}\n")
        f.write(f"Generated:   {datetime.now().strftime('%H:%M:%S')}\n")
        f.write("─"*90 + "\n\n")

        if total_flights == 0:
            f.write("┌─ NOTICE " + "─"*78 + "┐\n")
            f.write("│ NO FLIGHT DATA AVAILABLE FOR THIS REPORT PERIOD\n")
            f.write("│ Please check data files in /data directory\n")
            f.write("└" + "─"*88 + "┘\n\n")
            f.write("╔" + "═"*88 + "╗\n")
            f.write("║" + " "*35 + "END OF REPORT" + " "*40 + "║\n")
            f.write("╚" + "═"*88 + "╝\n")
            return path

        on_time_pct = (on_time_flights/total_flights*100) if total_flights > 0 else 0
        delayed_pct = (len(delayed_flights)/total_flights*100) if total_flights > 0 else 0

        f.write("┌─ EXECUTIVE SUMMARY " + "─"*68 + "┐\n")
        f.write(f"│ Total Flights Monitored          : {total_flights:>3} flights" + " "*38 + "│\n")
        f.write(f"│ On-Time Performance              : {on_time_flights:>3} flights ({on_time_pct:.1f}%)" + " "*28 + "│\n")
        f.write(f"│ Delayed Flights                  : {len(delayed_flights):>3} flights ({delayed_pct:.1f}%)" + " "*28 + "│\n")
        f.write(f"│ Total Delay Time                 : {total_delay_time:>4} minutes" + " "*36 + "│\n")
        f.write(f"│ Average Load Factor              : {avg_load:>5.1f}%" + " "*42 + "│\n")
        f.write(f"│ Critical Alerts                  : {len(critical_alerts):>3}" + " "*47 + "│\n")
        f.write(f"│ Warning Alerts                   : {len(warning_alerts):>3}" + " "*47 + "│\n")
        f.write(f"│ Crew Compliance Issues           : {len(crew_issues):>3}" + " "*47 + "│\n")
        f.write("└" + "─"*88 + "┘\n\n")

        if missing_flights:
            f.write("[!] INCOMPLETE DATA FOR:\n")
            for fid in missing_flights:
                f.write(f"    - {fid}\n")
            f.write("\n")

        f.write("┌─ DETAILED FLIGHT ANALYSIS " + "─"*61 + "┐\n\n")
        
        for fl in flights:
            fid = fl["flight_id"]
            route = f'{fl["route"]["origin"]} → {fl["route"]["destination"]}'
            d = delays_by_id.get(fid, {"delay_min": 0, "reasons": []})
            l = load_by_id.get(fid, {})
            c = crew_by_id.get(fid, {})

            if d["delay_min"] >= 60:
                delay_status = "[DELAYED-SEVERE]"
            elif d["delay_min"] > 0:
                delay_status = "[DELAYED]      "
            else:
                delay_status = "[ON-TIME]      "
            
            f.write(f"├─ {fid} | {fl['aircraft_id']:<10} | {route:<15} {delay_status}\n")
            f.write(f"│  Departure Time  : {fl['timestamp']}\n")
            f.write(f"│  Predicted Delay : {d['delay_min']} minutes\n")
            
            if d["reasons"]:
                f.write(f"│  Delay Factors   :\n")
                for reason in d["reasons"]:
                    f.write(f"│     • {reason}\n")
            
            if l:
                if l["overbooking_risk"]:
                    load_icon = "[OVERBOOKED]"
                elif l["under_utilized"]:
                    load_icon = "[LOW-UTIL]  "
                else:
                    load_icon = "[NORMAL]    "
                
                f.write(f"│  Passenger Load  : {load_icon} {l['predicted_load_pct']:.1f}% ({l['predicted_passengers']}/{fl['passenger']['capacity']} pax)\n")
                
                if l["overbooking_risk"]:
                    f.write(f"│     [!] OVERBOOKING RISK - Current bookings: {fl['passenger']['booked']}\n")
                if l["under_utilized"]:
                    f.write(f"│     [!] UNDER-UTILIZED FLIGHT - Consider route review\n")

            if c:
                f.write(f"│  Crew Status     : [NON-COMPLIANT]\n")
                for issue in c["issues"]:
                    f.write(f"│     • {issue}\n")
            else:
                f.write(f"│  Crew Status     : [COMPLIANT]\n")

            weather = fl["status"]["weather"]
            weather_risk = []
            if weather["crosswind"] > 35:
                weather_risk.append(f"High crosswind ({weather['crosswind']} knots)")
            if weather["thunderstorm"]:
                weather_risk.append("Thunderstorm")
            if weather["visibility"] < 2000:
                weather_risk.append(f"Low visibility ({weather['visibility']}m)")
            
            if weather_risk:
                f.write(f"│  Weather Risk    : [HIGH] {', '.join(weather_risk)}\n")
            else:
                f.write(f"│  Weather Risk    : [CLEAR]\n")

            f.write("│\n")

        f.write("└" + "─"*88 + "┘\n\n")

        f.write("┌─ AIRCRAFT HEALTH & MAINTENANCE " + "─"*55 + "┐\n")
        if not health_alerts:
            f.write("│  [OK] All aircraft systems operating normally\n")
        else:
            if critical_alerts:
                f.write("│  [CRITICAL] ISSUES (Immediate Action Required):\n")
                for lvl, msg in critical_alerts:
                    f.write(f"│     {msg}\n")
                f.write("│\n")
            
            if warning_alerts:
                f.write("│  [WARNING] ISSUES (Monitor Closely):\n")
                for lvl, msg in warning_alerts:
                    f.write(f"│     {msg}\n")
        f.write("└" + "─"*88 + "┘\n\n")

        f.write("┌─ OPERATIONAL RECOMMENDATIONS " + "─"*57 + "┐\n")
        
        if len(delayed_flights) > 0:
            f.write(f"│  1. DELAYS: {len(delayed_flights)} flights affected ({total_delay_time} total mins)\n")
            top_reasons = {}
            for d in delayed_flights:
                for r in d["reasons"]:
                    reason_type = r.split()[0]
                    top_reasons[reason_type] = top_reasons.get(reason_type, 0) + 1
            f.write(f"│     Primary causes: {', '.join(f'{k} ({v})' for k, v in sorted(top_reasons.items(), key=lambda x: x[1], reverse=True)[:3])}\n")
        
        if critical_alerts:
            f.write(f"│  2. MAINTENANCE: Ground {len(set([msg.split('|')[0].strip() for _, msg in critical_alerts]))} aircraft for inspection\n")
        
        if crew_issues:
            f.write(f"│  3. CREW: Arrange {len(crew_issues)} crew replacements for compliance\n")
        
        overbooked = [l for l in load_results if l.get("overbooking_risk")]
        if overbooked:
            f.write(f"│  4. CAPACITY: {len(overbooked)} flights overbooked - Arrange alternatives\n")
        
        if not (delayed_flights or critical_alerts or crew_issues or overbooked):
            f.write("│  [OK] All operations within normal parameters - Continue standard monitoring\n")
        
        f.write("└" + "─"*88 + "┘\n\n")

        f.write("╔" + "═"*88 + "╗\n")
        f.write("║" + " "*35 + "END OF REPORT" + " "*40 + "║\n")
        f.write("╚" + "═"*88 + "╝\n")

    return path
