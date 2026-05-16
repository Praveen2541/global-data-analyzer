import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connection import get_col

def clean():
    print("[CLEANING] Processing all collections...\n")

    # Clean world_population
    col = get_col("world_population")
    for doc in col.find({}):
        try:
            density = float(str(doc.get("density_per_km2", "0")).replace(",", "")) if doc.get("density_per_km2") not in ["N/A", "", None] else None
            area = float(str(doc.get("area_km2", "0")).replace(",", "")) if doc.get("area_km2") not in ["N/A", "", None] else None
            col.update_one({"_id": doc["_id"]}, {"$set": {
                "density_numeric": density,
                "area_numeric": area,
                "is_cleaned": True
            }})
        except:
            continue
    print(f"    [OK] world_population cleaned")

    # Clean world_gdp
    col = get_col("world_gdp")
    for doc in col.find({}):
        try:
            col.update_one({"_id": doc["_id"]}, {"$set": {"is_cleaned": True}})
        except:
            continue
    print(f"    [OK] world_gdp cleaned")

    # Clean countries_data
    col = get_col("countries_data")
    for doc in col.find({}):
        try:
            col.update_one({"_id": doc["_id"]}, {"$set": {"is_cleaned": True}})
        except:
            continue
    print(f"    [OK] countries_data cleaned")

    # Clean hockey_teams
    col = get_col("hockey_teams")
    for doc in col.find({}):
        try:
            col.update_one({"_id": doc["_id"]}, {"$set": {"is_cleaned": True}})
        except:
            continue
    print(f"    [OK] hockey_teams cleaned")

    print("\n[DONE] All collections cleaned successfully!")

if __name__ == "__main__":
    clean()