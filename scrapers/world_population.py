import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connection import get_col
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def run():
    col = get_col("world_population")
    col.drop()
    saved = 0

    print("[SCRAPING] worldometers.info - World Population by Country")
    url = "https://www.worldometers.info/world-population/population-by-country/"

    try:
        res = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(res.text, "lxml")
        table = soup.find("table", {"id": "example2"})

        if not table:
            print("[WARN] Table not found, trying alternative selector")
            table = soup.find("table")

        rows = table.find_all("tr")[1:] if table else []
        print(f"         Found {len(rows)} countries")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 5:
                continue
            try:
                def clean(val):
                    return val.replace(",", "").replace("%", "").strip()

                rank = int(clean(cols[0].text)) if clean(cols[0].text).isdigit() else None
                country = cols[1].text.strip()
                population = int(clean(cols[2].text)) if clean(cols[2].text).replace("-","").isdigit() else None
                yearly_change = clean(cols[3].text)
                net_change = clean(cols[4].text)
                density = clean(cols[5].text) if len(cols) > 5 else "N/A"
                area = clean(cols[6].text) if len(cols) > 6 else "N/A"
                region = cols[8].text.strip() if len(cols) > 8 else "N/A"

                doc = {
                    "source": "worldometers.info",
                    "rank": rank,
                    "country": country,
                    "population": population,
                    "yearly_change_pct": yearly_change,
                    "net_change": net_change,
                    "density_per_km2": density,
                    "area_km2": area,
                    "region": region,
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