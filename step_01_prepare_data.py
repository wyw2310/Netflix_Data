from typing import Any, Optional

type CsvRecord = dict[str, str]
type Record = dict[str, Any]

def prep_dirs():
    import os

    os.makedirs("data/downloaded", exist_ok=True)
    os.makedirs("data/extracted", exist_ok=True)
    os.makedirs("data/enriched", exist_ok=True)
    os.makedirs("data/normalised", exist_ok=True)

def download_movies_and_tv_shows_from_kaggle_data(source_url: str, target_path):
    import requests

    response = requests.get(source_url)
    with open(target_path, 'wb') as file:
        file.write(response.content)
    print(f"File downloaded: {target_path}")


def extract_csv_file(zip_file_path: str, csv_file_name: str, csv_file_path: str):
    from zipfile import ZipFile

    with ZipFile(zip_file_path, 'r') as zip_ref:
        if csv_file_name in zip_ref.namelist():
            zip_ref.extract(csv_file_name, csv_file_path)
            print(f"Extracted CSV file to {csv_file_path}/{csv_file_name}")
        else:
            print(f"File {csv_file_name} not found in the zip archive.")


def merge_input_data() -> list[Record]:
    import csv
    from glob import glob

    merged_records: list[Record] = []
    for csv_file in glob("data/extracted/*.csv"):
        with open(csv_file, "r", encoding="utf-8") as f:
            platform = csv_file.removeprefix("data/extracted/").removeprefix("data/extracted\\").removesuffix("_titles.csv")
            records = [{"listing_id": f"{platform}-{record.get("show_id")}", "platform": platform, **record} for record in csv.DictReader(f)]
            merged_records += records
    
    return merged_records


def enrich_record(record: CsvRecord) -> Record:
    from datetime import datetime

    def apply_if_not_null(field_name: str, f):
        value = record.get(field_name, "").strip()
        if value:
            return f(value)
        else:
            return None
    
    def split_by_comma(value: str) -> list[str]:
        return [s.strip() for s in value.split(",")]
    
    def get_duration_or_seasons(duration_str: str) -> tuple[int, str]:
        parts = duration_str.split(" ", 1)
        return int(parts[0].strip()), parts[-1].lower()
    
    def get_movie_duration(duration_str: str) -> Optional[int]:
        duration_or_seasons, unit = get_duration_or_seasons(duration_str)
        return duration_or_seasons if "min" in unit else None
    
    def get_tv_series_seasons(duration_str: str) -> Optional[int]:
        duration_or_seasons, unit = get_duration_or_seasons(duration_str)
        return duration_or_seasons if "seasons" in unit else None


    release_year = apply_if_not_null("release_year", int)
    rating = apply_if_not_null("rating", lambda r: r)
    date_added = apply_if_not_null("date_added", lambda dts: datetime.strptime(dts, "%B %d, %Y").date())
    years_after_release = date_added.year - release_year if date_added else None
    directors = apply_if_not_null("director", split_by_comma)
    casts = apply_if_not_null("cast", split_by_comma)
    producer_countries = apply_if_not_null("country", split_by_comma)
    categories = apply_if_not_null("listed_in", split_by_comma)
    return {
        **record,
        "directors": directors,
        "casts": casts,
        "producer_countries": producer_countries,
        "date_added": date_added.isoformat()[:10] if date_added else None,
        "added_year": date_added.year if date_added else None,
        "added_month": date_added.month if date_added else None,
        "added_day_of_month": date_added.day if date_added else None,
        "added_day_of_week": date_added.weekday() + 1 if date_added else None,
        "release_year": release_year,
        "rating": rating,
        "years_after_release": years_after_release,
        "movie_duration": apply_if_not_null("duration", get_movie_duration),
        "tv_series_seasons": apply_if_not_null("duration", get_tv_series_seasons),
        "categories": categories,
    }

def write_enriched_records(records: list[Record]):
    with open("data/enriched/enriched.json", "w") as f:
        import json
        f.write(json.dumps(records, indent=4))


def normalise_records(enriched_records: list[Record]):
    import json

    listings = [{
        "listing_id": r.get("listing_id"),
        "platform": r.get("platform"),
        "show_id": r.get("show_id"),
        "type": r.get("type"),
        "title": r.get("title"),
        "date_added": r.get("date_added"),
        "added_year": r.get("added_year"),
        "added_month": r.get("added_month"),
        "added_day_of_month": r.get("added_day_of_month"),
        "added_day_of_week": r.get("added_day_of_week"),
        "release_year": r.get("release_year"),
        "years_after_release": r.get("years_after_release"),
        "rating": r.get("rating"),
        "movie_duration": r.get("movie_duration"),
        "tv_series_seasons": r.get("tv_series_seasons"),
        "description": r.get("description"),
    } for r in enriched_records]
    with open("data/normalised/listings.json", "w") as f:
        f.write(json.dumps(listings, indent=4))

    listing_directors = []
    listing_casts = []
    listing_producer_countries = []
    listing_categories = []
    for r in enriched_records:
        listing_id = r["listing_id"]
        directors = list(set(r.get("directors") or []))
        casts = list(set(r.get("casts") or []))
        producer_countries = list(set(r.get("producer_countries") or []))
        categories = list(set(r.get("categories") or []))
        for director in directors:
            listing_directors.append({"listing_id": listing_id, "director": director})
        for cast in casts:
            listing_casts.append({"listing_id": listing_id, "cast": cast})
        for producer_country in producer_countries:
            listing_producer_countries.append({"listing_id": listing_id, "producer_country": producer_country})
        for category in categories:
            listing_categories.append({"listing_id": listing_id, "category": category})
    with open("data/normalised/listing_directors.json", "w") as f:
        f.write(json.dumps(listing_directors, indent=4))
    with open("data/normalised/listing_casts.json", "w") as f:
        f.write(json.dumps(listing_casts, indent=4))
    with open("data/normalised/listing_producer_countries.json", "w") as f:
        f.write(json.dumps(listing_producer_countries, indent=4))
    with open("data/normalised/listing_categories.json", "w") as f:
        f.write(json.dumps(listing_categories, indent=4))


if __name__ == "__main__":
    prep_dirs()
    for url, zip_file_path, csv_file_name in [
        [
            "https://www.kaggle.com/api/v1/datasets/download/shivamb/netflix-shows",
            "data/downloaded/netflix-movies-and-tv-shows.zip",
            "netflix_titles.csv"
        ],
        [
            "https://www.kaggle.com/api/v1/datasets/download/shivamb/amazon-prime-movies-and-tv-shows",
            "data/downloaded/amazon-prime-movies-and-tv-shows.zip",
            "amazon_prime_titles.csv"
        ],
        [
            "https://www.kaggle.com/api/v1/datasets/download/shivamb/disney-movies-and-tv-shows",
            "data/downloaded/disney-movies-and-tv-shows.zip",
            "disney_plus_titles.csv"
        ],
    ]:
        print("==================================================")
        download_movies_and_tv_shows_from_kaggle_data(source_url=url, target_path=zip_file_path)
        extract_csv_file(zip_file_path, csv_file_name, csv_file_path="data/extracted")
        print("==================================================")
        print()
    
    merged_records = merge_input_data()
    enriched_records = [*map(enrich_record, merged_records)]
    write_enriched_records(enriched_records)
    normalise_records(enriched_records)
    