from scrapers.world_population import run as scrape_population
from scrapers.world_gdp import run as scrape_gdp
from scrapers.countries_data import run as scrape_countries
from scrapers.hockey_teams import run as scrape_hockey
from reports.cleaner import clean
from reports.analytics import run_all
from datetime import datetime

if __name__ == "__main__":
    print("=" * 60)
    print("   GLOBAL DATA ANALYZER")
    print("   Starting data collection pipeline...")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    print("\n>> PHASE 1: SCRAPING")
    scrape_population()
    scrape_gdp()
    scrape_countries()
    scrape_hockey()

    print("\n>> PHASE 2: CLEANING")
    clean()

    print("\n>> PHASE 3: ANALYTICS")
    run_all()

    print(f"\nPipeline completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")