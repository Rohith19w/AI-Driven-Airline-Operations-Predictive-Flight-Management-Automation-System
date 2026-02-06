def show_dashboard(flights, delay_results, health_alerts, crew_issues, load_results):
    total = len(flights)
    delayed = [d for d in delay_results if d["delay_min"] > 0]
    critical = [a for a in health_alerts if a[0] == "CRITICAL"]
    warnings = [a for a in health_alerts if a[0] == "WARN"]

    avg_load = 0.0
    if load_results:
        avg_load = sum(x["predicted_load_pct"] for x in load_results) / len(load_results)

    route_counts = {}
    for f in flights:
        key = f'{f["route"]["origin"]}->{f["route"]["destination"]}'
        route_counts[key] = route_counts.get(key, 0) + 1
    popular_route = max(route_counts, key=route_counts.get) if route_counts else "N/A"

    total_delay_mins = sum(d["delay_min"] for d in delay_results)
    
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " "*20 + "AIRLINE OPERATIONS CONTROL CENTER" + " "*25 + "║")
    print("╚" + "═"*78 + "╝")
    
    print("\n┌─ OPERATIONS SUMMARY " + "─"*57 + "┐")
    print(f"│ Total Flights Monitored       : {total:>3} flights")
    print(f"│ Flights On-Time               : {total - len(delayed):>3} flights")
    print(f"│ Flights Delayed               : {len(delayed):>3} flights")
    print(f"│ Total Delay Time              : {total_delay_mins:>3} minutes")
    print(f"│ Average Load Factor           : {avg_load:>5.1f}%")
    print(f"│ Popular Route                 : {popular_route}")
    print("└" + "─"*78 + "┘")

    print("\n┌─ ALERT SUMMARY " + "─"*61 + "┐")
    print(f"│ [CRITICAL] Alerts             : {len(critical):>3}")
    print(f"│ [WARNING]  Alerts             : {len(warnings):>3}")
    print(f"│ Crew Compliance Issues        : {len(crew_issues):>3}")
    print("└" + "─"*78 + "┘")

    if delayed:
        print("\n┌─ DELAY ANALYSIS " + "─"*60 + "┐")
        for d in sorted(delayed, key=lambda x: x["delay_min"], reverse=True):
            if d["delay_min"] >= 120:
                severity = "[SEVERE]  "
            elif d["delay_min"] >= 60:
                severity = "[MODERATE]"
            else:
                severity = "[MINOR]   "
            
            print(f"│ {d['flight_id']:<8} {severity} {d['delay_min']:>3} min")
            if d["reasons"]:
                reasons_wrapped = d["reasons"][:3]
                for r in reasons_wrapped:
                    print(f"│          └─ {r:<60} │")
        print("└" + "─"*78 + "┘")

    if critical or warnings:
        print("\n┌─ AIRCRAFT HEALTH STATUS " + "─"*52 + "┐")
        if critical:
            print("│ [CRITICAL] ISSUES:")
            for lvl, msg in critical:
                parts = msg.split("|")
                if len(parts) >= 2:
                    fid = parts[0].strip()
                    issue = parts[1].strip()
                    print(f"│    [{fid}] {issue:<60} │")
        if warnings:
            print("│ [WARNING] ISSUES:")
            for lvl, msg in warnings[:3]:
                parts = msg.split("|")
                if len(parts) >= 2:
                    fid = parts[0].strip()
                    issue = parts[1].strip()
                    print(f"│    [{fid}] {issue:<60} │")
        print("└" + "─"*78 + "┘")

    if crew_issues:
        print("\n┌─ CREW COMPLIANCE ISSUES " + "─"*52 + "┐")
        for item in crew_issues:
            print(f"│ Flight: {item['flight_id']:<10}")
            for issue in item["issues"]:
                print(f"│    [!] {issue:<65} │")
        print("└" + "─"*78 + "┘")

    overbooked = [l for l in load_results if l.get("overbooking_risk")]
    underutilized = [l for l in load_results if l.get("under_utilized")]
    
    if overbooked or underutilized:
        print("\n┌─ PASSENGER LOAD ISSUES " + "─"*53 + "┐")
        if overbooked:
            print("│ [OVERBOOKED] RISK:")
            for l in overbooked:
                print(f"│    {l['flight_id']:<10} Load: {l['predicted_load_pct']:>5.1f}%")
        if underutilized:
            print("│ [UNDER-UTILIZED]:")
            for l in underutilized:
                print(f"│    {l['flight_id']:<10} Load: {l['predicted_load_pct']:>5.1f}%")
        print("└" + "─"*78 + "┘")

    print("\n┌─ RECOMMENDATIONS " + "─"*59 + "┐")
    recs = []
    if len(delayed) > total * 0.5:
        recs.append("High delay rate detected - Review weather & operational procedures")
    if critical:
        recs.append("IMMEDIATE: Ground aircraft with critical health issues")
    if crew_issues:
        recs.append("Schedule crew replacements for non-compliant assignments")
    if overbooked:
        recs.append("Arrange alternate flights for overbooked passengers")
    if not recs:
        recs.append("All systems operating normally - Continue monitoring")
    
    for i, rec in enumerate(recs, 1):
        print(f"│ {i}. {rec:<74} │")
    print("└" + "─"*78 + "┘\n")
