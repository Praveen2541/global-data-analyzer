import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connection import get_col
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def run():
    col = get_col("world_gdp")
    col.drop()
    saved = 0

    print("[SCRAPING] worldometers.info - GDP by Country")
    url = "https://www.worldometers.info/gdp/gdp-by-country/"

    try:
        res = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(res.text, "lxml")
        table = soup.find("table")
        rows = table.find_all("tr")[1:] if table else []
        print(f"         Found {len(rows)} countries")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue
            try:
                def clean(val):
                    return val.replace(",", "").replace("$", "").replace("%", "").strip()

                rank = cols[0].text.strip()
                country = cols[1].text.strip()
                gdp_usd = clean(cols[2].text)
                gdp_growth = clean(cols[3].text)
                population = clean(cols[4].text) if len(cols) > 4 else "N/A"
                gdp_per_capita = clean(cols[5].text) if len(cols) > 5 else "N/A"
                share_world = clean(cols[6].text) if len(cols) > 6 else "N/A"

                try:
                    gdp_numeric = float(gdp_usd) if gdp_usd else None
                except:
                    gdp_numeric = None

                try:
                    gdp_per_capita_numeric = float(gdp_per_capita) if gdp_per_capita else None
                except:
                    gdp_per_capita_numeric = None

                doc = {
                    "source": "worldometers.info",
                    "rank": rank,
                    "country": country,
                    "gdp_usd": gdp_usd,
                    "gdp_numeric": gdp_numeric,
                    "gdp_growth_pct": gdp_growth,
                    "population": population,
                    "gdp_per_capita": gdp_per_capita,
                    "gdp_per_capita_numeric": gdp_per_capita_numeric,
                    "share_of_world_gdp_pct": share_world,
                    "scraped_at": datetime.now()
                }
                col.insert_one(doc)
                saved += 1
            except:
                continue

    except Exception as e:
        print(f"[ERROR] {e}")

    print(f"         Saved {saved} records to MongoDB\n")
    return saved

if __name__ == "__main__":
    run()