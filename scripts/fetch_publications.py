#!/usr/bin/env python3
"""
Fetch publications for a list of authors from the ORCID public API and
write them to a Jekyll _data file (_data/publications.yml).

Usage:
    python fetch_publications.py

Config:
    scripts/authors.yml   - list of {name, orcid} entries

Output:
    _data/publications.yml
"""

import sys
import time
import yaml
import requests
from pathlib import Path

ORCID_API_BASE = "https://pub.orcid.org/v3.0"
HEADERS = {"Accept": "application/json"}
REQUEST_TIMEOUT = 20
RETRY_COUNT = 3
RETRY_DELAY = 2  # seconds

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
AUTHORS_FILE = SCRIPT_DIR / "authors.yml"
OUTPUT_FILE = REPO_ROOT / "_data" / "publications.yml"


def api_get(url):
    """GET with basic retry logic."""
    last_err = None
    for attempt in range(1, RETRY_COUNT + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            last_err = e
            print(f"  Attempt {attempt}/{RETRY_COUNT} failed for {url}: {e}", file=sys.stderr)
            time.sleep(RETRY_DELAY)
    print(f"  Giving up on {url}: {last_err}", file=sys.stderr)
    return None


def extract_external_id(external_ids, id_type):
    """Pull a specific external identifier (e.g. 'doi') from a work summary."""
    if not external_ids:
        return None
    for ext in external_ids.get("external-id", []):
        if ext.get("external-id-type", "").lower() == id_type.lower():
            url_info = ext.get("external-id-url")
            if url_info and url_info.get("value"):
                return url_info["value"]
            return ext.get("external-id-value")
    return None


def parse_work_summary(summary, fallback_author_name):
    title_container = summary.get("title") or {}
    title = (title_container.get("title") or {}).get("value")
    if not title:
        return None

    pub_date = summary.get("publication-date") or {}
    year = (pub_date.get("year") or {}).get("value")

    journal = summary.get("journal-title")
    venue = journal.get("value") if journal else None

    work_type = summary.get("type")

    external_ids = summary.get("external-ids")
    doi_url = extract_external_id(external_ids, "doi")

    put_code = summary.get("put-code")
    orcid_path = summary.get("path") or ""
    # Fallback link straight to the ORCID record if no DOI is present
    orcid_url = f"https://orcid.org{orcid_path}" if orcid_path else None

    url = doi_url or orcid_url

    return {
        "title": title.strip(),
        "year": int(year) if year and str(year).isdigit() else None,
        "venue": venue.strip() if venue else None,
        "type": work_type,
        "url": url,
        "lab_author": fallback_author_name,
        "put_code": put_code,
    }


def fetch_author_works(orcid_id, display_name):
    print(f"Fetching works for {display_name} ({orcid_id})...")
    data = api_get(f"{ORCID_API_BASE}/{orcid_id}/works")
    if not data:
        print(f"  No data returned for {orcid_id}", file=sys.stderr)
        return []

    works = []
    for group in data.get("group", []):
        summaries = group.get("work-summary", [])
        if not summaries:
            continue
        # Each group can contain duplicate summaries from different sources
        # (e.g. Crossref + publisher). Take the first as representative.
        parsed = parse_work_summary(summaries[0], display_name)
        if parsed:
            works.append(parsed)

    print(f"  Found {len(works)} works")
    return works


def dedupe(all_works):
    """Merge duplicate works across authors (same DOI/title), combining lab authors."""
    seen = {}
    order = []
    for work in all_works:
        key = (work["url"] or "").lower() or work["title"].lower()
        if key in seen:
            existing = seen[key]
            if work["lab_author"] not in existing["lab_authors"]:
                existing["lab_authors"].append(work["lab_author"])
        else:
            work["lab_authors"] = [work["lab_author"]]
            del work["lab_author"]
            del work["put_code"]
            seen[key] = work
            order.append(key)
    return [seen[k] for k in order]


def main():
    if not AUTHORS_FILE.exists():
        print(f"ERROR: {AUTHORS_FILE} not found.", file=sys.stderr)
        sys.exit(1)

    with open(AUTHORS_FILE) as f:
        config = yaml.safe_load(f) or {}

    authors = config.get("authors", [])
    if not authors:
        print("ERROR: no authors listed in authors.yml", file=sys.stderr)
        sys.exit(1)

    all_works = []
    for author in authors:
        orcid_id = author.get("orcid")
        name = author.get("name", orcid_id)
        if not orcid_id:
            print(f"Skipping entry with no ORCID iD: {author}", file=sys.stderr)
            continue
        all_works.extend(fetch_author_works(orcid_id, name))

    if not all_works:
        print("ERROR: no works fetched for any author; aborting without overwriting output.", file=sys.stderr)
        sys.exit(1)

    deduped = dedupe(all_works)

    # Sort newest first; undated works go last
    deduped.sort(key=lambda w: (w["year"] is None, -(w["year"] or 0), w["title"]))

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        yaml.dump(deduped, f, sort_keys=False, allow_unicode=True, width=1000)

    print(f"\nWrote {len(deduped)} unique publications to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
