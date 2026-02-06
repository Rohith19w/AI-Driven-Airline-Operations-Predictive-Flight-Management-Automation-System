def show_dashboard(flights, delay_results, health_alerts, crew_issues, load_results):
    total = len(flights)
    delayed = [d for d in delay_results if d["delay_min"] > 0]
    critical = [a for a in health_alerts if a[0] == "CRITICAL"]

    avg_load = 0.0
    if load_results:
        avg_load = sum(x["predicted_load_pct"] for x in load_results) / len(load_results)

    route_counts = {}
    for f in flights:
        key = f'{f["route"]["origin"]}->{f["route"]["destination"]}'
        route_counts[key] = route_counts.get(key, 0) + 1
    popular_route = max(route_counts, key=route_counts.get) if route_counts else "N/A"

    print("\n" + "="*50)
    print("   AIRLINE OPERATIONS CONTROL CENTER")
    print("="*50)
    print(f"Flights monitored: {total}")
    print(f"Predicted delays: {len(delayed)}")
    print(f"Critical alerts: {len(critical)}")
    print(f"Crew issues: {len(crew_issues)}")
    print(f"Avg predicted load: {avg_load:.1f}%")
    print(f"Popular route: {popular_route}")
    print("="*50)

    if delayed:
        print("\nDELAYS DETECTED:")
        for d in delayed[:10]:
            rs = "; ".join(d["reasons"]) if d["reasons"] else "Unknown"
            print(f'  {d["flight_id"]}: {d["delay_min"]}min → {rs}')

    if critical:
        print("\nCRITICAL ALERTS:")
        for lvl, msg in critical[-5:]:
            print(f"  {lvl}: {msg}")

    if crew_issues:
        print("\nCREW ISSUES:")
        for item in crew_issues[:10]:
            print(f'  {item["flight_id"]}: {"; ".join(item["issues"])}')

    print("\n" + "="*50 + "\n")
