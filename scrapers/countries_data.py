import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connection import get_col
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def run():
    col = get_col("countries_data")
    col.drop()
    saved = 0

    print("[SCRAPING] scrapethissite.com - Countries of the World")
    url = "https://www.scrapethissite.com/pages/simple/"

    try:
        res = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(res.text, "lxml")
        countries = soup.find_all("div", class_="country")
        print(f"         Found {len(countries)} countries")

        for country in countries:
            try:
                name = country.find("h3", class_="country-name")
                capital = country.find("span", class_="country-capital")
                population = country.find("span", class_="country-population")
                area = country.find("span", class_="country-area")

                pop_val = float(population.text.strip()) if population else None
                area_val = float(area.text.strip()) if area else None
                pop_density = round(pop_val / area_val, 2) if pop_val and area_val and area_val > 0 else None

                doc = {
                    "source": "scrapethissite.com",
                    "country": name.text.strip() if name else "N/A",
                    "capital": capital.text.strip() if capital else "N/A",
                    "population": pop_val,
                    "area_km2": area_val,
                    "population_density": pop_density,
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