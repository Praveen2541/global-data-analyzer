import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connection import get_col
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

PAGES = range(1, 6)

def run():
    col = get_col("hockey_teams")
    col.drop()
    saved = 0

    print("[SCRAPING] scrapethissite.com - Hockey Teams")

    for page in PAGES:
        url = f"https://www.scrapethissite.com/pages/forms/?page_num={page}"
        try:
            res = requests.get(url, headers=HEADERS, timeout=20)
            soup = BeautifulSoup(res.text, "lxml")
            rows = soup.find_all("tr", class_="team")
            print(f"         Page {page}: Found {len(rows)} teams")

            for row in rows:
                try:
                    name = row.find("td", class_="name")
                    year = row.find("td", class_="year")
                    wins = row.find("td", class_="wins")
                    losses = row.find("td", class_="losses")
                    ot_losses = row.find("td", class_="ot-losses")
                    pct = row.find("td", class_="pct")
                    gf = row.find("td", class_="gf")
                    ga = row.find("td", class_="ga")
                    diff = row.find("td", class_="diff")

                    def to_int(tag):
                        try:
                            return int(tag.text.strip())
                        except:
                            return None

                    def to_float(tag):
                        try:
                            return float(tag.text.strip())
                        except:
                            return None

                    doc = {
                        "source": "scrapethissite.com",
                        "team_name": name.text.strip() if name else "N/A",
                        "year": to_int(year),
                        "wins": to_int(wins),
                        "losses": to_int(losses),
                        "ot_losses": to_int(ot_losses),
                        "win_pct": to_float(pct),
                        "goals_for": to_int(gf),
                        "goals_against": to_int(ga),
                        "goal_diff": to_int(diff),
                        "scraped_at": datetime.now()
                    }
                    col.insert_one(doc)
                    saved += 1
                except:
                    continue

        except Exception as e:
            print(f"[ERROR] Page {page}: {e}")
            continue

    print(f"         Saved {saved} records to MongoDB\n")
    return saved

if __name__ == "__main__":
    run()