import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connection import get_col
from datetime import datetime

LINE = "-" * 60

def report_population():
    print(f"\n{LINE}")
    print("REPORT 1 >> TOP 10 MOST POPULATED COUNTRIES")
    print(LINE)
    col = get_col("world_population")
    results = list(col.find(
        {"population": {"$ne": None}},
        {"country": 1, "population": 1, "yearly_change_pct": 1, "rank": 1}
    ).sort("population", -1).limit(10))

    if results:
        for i, r in enumerate(results, 1):
            pop = f"{r.get('population', 0):,}"
            print(f"  {i:2}. {r.get('country', 'N/A'):30} | Population: {pop:15} | Yearly Change: {r.get('yearly_change_pct', 'N/A')}")
    else:
        print("  No data available")

def report_gdp():
    print(f"\n{LINE}")
    print("REPORT 2 >> TOP 10 RICHEST COUNTRIES BY GDP")
    print(LINE)
    col = get_col("world_gdp")
    results = list(col.find(
        {},
        {"country": 1, "gdp_usd": 1, "gdp_per_capita": 1, "gdp_growth_pct": 1}
    ).limit(10))

    if results:
        for i, r in enumerate(results, 1):
            print(f"  {i:2}. {r.get('country', 'N/A'):30} | GDP: ${r.get('gdp_usd', 'N/A'):15} | Per Capita: ${r.get('gdp_per_capita', 'N/A')}")
    else:
        print("  No data available")

def report_density():
    print(f"\n{LINE}")
    print("REPORT 3 >> TOP 10 MOST DENSELY POPULATED COUNTRIES")
    print(LINE)
    col = get_col("countries_data")
    results = list(col.find(
        {"population_density": {"$ne": None, "$gt": 0}},
        {"country": 1, "capital": 1, "population": 1, "population_density": 1}
    ).sort("population_density", -1).limit(10))

    if results:
        for i, r in enumerate(results, 1):
            print(f"  {i:2}. {r.get('country', 'N/A'):30} | Capital: {r.get('capital', 'N/A'):20} | Density: {r.get('population_density', 0):,.1f}/km2")
    else:
        print("  No data available")

def report_hockey():
    print(f"\n{LINE}")
    print("REPORT 4 >> TOP 10 HOCKEY TEAMS BY WINS (ALL TIME)")
    print(LINE)
    col = get_col("hockey_teams")
    pipeline = [
        {"$match": {"wins": {"$ne": None}}},
        {"$group": {
            "_id": "$team_name",
            "total_wins": {"$sum": "$wins"},
            "total_losses": {"$sum": "$losses"},
            "avg_goals_for": {"$avg": "$goals_for"},
            "avg_win_pct": {"$avg": "$win_pct"},
            "seasons": {"$sum": 1}
        }},
        {"$sort": {"total_wins": -1}},
        {"$limit": 10}
    ]
    results = list(col.aggregate(pipeline))
    if results:
        for i, r in enumerate(results, 1):
            print(f"  {i:2}. {str(r['_id']):35} | Wins: {r['total_wins']:4} | Losses: {r['total_losses']:4} | Avg Goals: {r.get('avg_goals_for', 0):.1f}")
    else:
        print("  No data available")

def report_region_summary():
    print(f"\n{LINE}")
    print("REPORT 5 >> TOTAL POPULATION BY CONTINENT")
    print(LINE)

    # Since worldometers scraping gave us median age instead of region
    # We use countries_data collection grouped by population ranges
    col = get_col("countries_data")

    # Define population tiers
    tiers = [
        ("Large Nations (>100M)", 100000000, float('inf')),
        ("Medium-Large Nations (10M-100M)", 10000000, 100000000),
        ("Medium Nations (1M-10M)", 1000000, 10000000),
        ("Small Nations (<1M)", 0, 1000000),
    ]

    total_world = 0
    results_list = []
    for label, low, high in tiers:
        results = list(col.find({
            "population": {"$gte": low, "$lt": high}
        }))
        count = len(results)
        total_pop = sum(r.get("population", 0) or 0 for r in results)
        avg_pop = total_pop / count if count > 0 else 0
        total_world += total_pop
        results_list.append((label, count, total_pop, avg_pop))

    for label, count, total_pop, avg_pop in results_list:
        print(f"  {label:35} | Countries: {count:3} | Total Pop: {total_pop:>15,} | Avg: {avg_pop:>12,.0f}")

    print(f"\n  {'TOTAL WORLD POPULATION':35} | {total_world:,}")

def report_summary():
    print(f"\n{LINE}")
    print("REPORT 6 >> DATABASE SUMMARY")
    print(LINE)
    collections = ["world_population", "world_gdp", "countries_data", "hockey_teams"]
    sources = [
        "worldometers.info (Population)",
        "worldometers.info (GDP)",
        "scrapethissite.com (Countries)",
        "scrapethissite.com (Hockey)"
    ]
    total = 0
    for col_name, source in zip(collections, sources):
        count = get_col(col_name).count_documents({})
        total += count
        print(f"  {source:45} >> {count} records")
    print(f"\n  TOTAL RECORDS IN MONGODB   >> {total}")
    print(f"  REPORT GENERATED AT        >> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def run_all():
    print("\n" + "=" * 60)
    print("   GLOBAL DATA INTELLIGENCE REPORT")
    print("   Data Management Project -- SRH University Hamburg")
    print("=" * 60)
    report_population()
    report_gdp()
    report_density()
    report_hockey()
    report_region_summary()
    report_summary()
    print(f"\n{'=' * 60}")
    print("   ALL REPORTS GENERATED SUCCESSFULLY")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    run_all()