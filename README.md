# Global Data Analyzer

> A Python-based web scraping pipeline that collects, cleans, and analyzes
> real-world data from multiple sources using BeautifulSoup and MongoDB.

---

## Data Sources

| # | Website | Data Collected |
|---|---------|----------------|
| 1 | [Worldometers - Population](https://www.worldometers.info/world-population/population-by-country/) | Country populations, density, yearly change |
| 2 | [Worldometers - GDP](https://www.worldometers.info/gdp/gdp-by-country/) | GDP, GDP per capita, growth rate |
| 3 | [ScrapeThisSite - Countries](https://www.scrapethissite.com/pages/simple/) | Countries, capitals, area |
| 4 | [ScrapeThisSite - Hockey](https://www.scrapethissite.com/pages/forms/) | Hockey teams, wins, losses, goals |

---

## Business Objectives & Reports

| Report | Description |
|--------|-------------|
| Report 1 | Top 10 most populated countries with yearly growth |
| Report 2 | Top 10 richest countries by GDP and GDP per capita |
| Report 3 | Top 10 most densely populated countries |
| Report 4 | Top 10 hockey teams ranked by total wins |
| Report 5 | World population grouped by nation size |
| Report 6 | Complete database summary |

---

## Tech Stack

```
Python 3.13
├── requests          - HTTP requests
├── beautifulsoup4    - HTML parsing
├── pymongo           - MongoDB driver
├── pandas            - Data processing
├── python-dotenv     - Environment variables
└── certifi           - SSL certificates

MongoDB Atlas         - Cloud database (AWS Frankfurt)
```

---

## Project Structure

```
global-data-analyzer/
│
├── scrapers/
│   ├── __init__.py
│   ├── world_population.py
│   ├── world_gdp.py
│   ├── countries_data.py
│   └── hockey_teams.py
│
├── database/
│   ├── __init__.py
│   └── connection.py
│
├── reports/
│   ├── __init__.py
│   ├── cleaner.py
│   └── analytics.py
│
├── output-screenshots/
│   ├── scraping.png
│   ├── cleaning.png
│   └── analytics.png
│
├── .env
├── .gitignore
├── requirements.txt
├── prompts.txt
├── run.py
└── README.md
```

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Praveen2541/global-data-analyzer.git
cd global-data-analyzer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure MongoDB
Create a `.env` file in the root folder:
```
MONGODB_URI=your_mongodb_connection_string
DB_NAME=globaldata_db
```

### 4. Run the full pipeline
```bash
python run.py
```

### 5. Run only analytics
```bash
python reports/analytics.py
```

### 6. Test MongoDB connection
```bash
python database/connection.py
```

---

## MongoDB Collections

| Collection | Source | Records |
|------------|--------|---------|
| `world_population` | worldometers.info | 234 |
| `world_gdp` | worldometers.info | 218 |
| `countries_data` | scrapethissite.com | 250 |
| `hockey_teams` | scrapethissite.com | 125 |
| **Total** | | **827** |

---

## Sample Output

```
REPORT 1 >> TOP 10 MOST POPULATED COUNTRIES
  1. India          | Population: 1,476,625,576 | Yearly Change: 0.87%
  2. China          | Population: 1,412,914,089 | Yearly Change: -0.22%
  3. United States  | Population: 349,035,494   | Yearly Change: 0.51%

REPORT 2 >> TOP 10 RICHEST COUNTRIES BY GDP
  1. United States  | GDP: $32.38 trillion | Per Capita: $94,430
  2. China          | GDP: $20.85 trillion | Per Capita: $14,874
  3. Germany        | GDP: $5.45 trillion  | Per Capita: $65,303
```

---

## Author

**Praveen Kumar Reddy**
SRH University Hamburg — Data Management Project
Summer Semester 2026