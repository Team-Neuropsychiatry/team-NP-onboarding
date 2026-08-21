#!/usr/bin/env python3
"""
Fetch publications for a list of authors from the ORCID public API,
enrich them with full citation data (author list, journal, volume/issue/
pages) from Crossref via each work's DOI, and write the result to a
Jekyll _data file (_data/publications.yml).

Only publications from the last YEARS_TO_KEEP years are kept.

Usage:
    python fetch_publications.py

Config:
    scripts/authors.yml   - list of {name, orcid} entries + contact_email

Output:
    _data/publications.yml
"""

import re
import sys
import time
import datetime
import yaml
import requests
from pathlib import Path

ORCID_API_BASE = "https://pub.orcid.org/v3.0"
CROSSREF_API_BASE = "https://api.crossref.org/works"
ORCID_HEADERS = {"Accept": "application/json"}
REQUEST_TIMEOUT = 20
RETRY_COUNT = 3
RETRY_DELAY = 2  # seconds
YEARS_TO_KEEP = 5

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
AUTHORS_FILE = SCRIPT_DIR / "authors.yml"
OUTPUT_FILE = REPO_ROOT / "_data" / "publications.yml"


def api_get(url, headers):
    """GET with basic retry logic. Returns parsed JSON or None."""
    last_err = None
    for attempt in range(1, RETRY_COUNT + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            last_err = e
            print(f"    Attempt {attempt}/{RETRY_COUNT} failed for {url}: {e}", file=sys.stderr)
            time.sleep(RETRY_DELAY)
    print(f"    Giving up on {url}: {last_err}", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# ORCID: discover which works belong to the lab
# ---------------------------------------------------------------------------

def extract_doi(external_ids):
    if not external_ids:
        return None
    for ext in external_ids.get("external-id", []):
        if ext.get("external-id-type", "").lower() == "doi":
            return ext.get("external-id-value")
    return None


def fetch_author_works(orcid_id, display_name):
    print(f"Fetching works for {display_name} ({orcid_id})...")
    data = api_get(f"{ORCID_API_BASE}/{orcid_id}/works", ORCID_HEADERS)
    if not data:
        print(f"  No data returned for {orcid_id}", file=sys.stderr)
        return []

    works = []
    for group in data.get("group", []):
        summaries = group.get("work-summary", [])
        if not summaries:
            continue
        summary = summaries[0]  # representative summary for this group
        title = ((summary.get("title") or {}).get("title") or {}).get("value")
        if not title:
            continue
        pub_date = summary.get("publication-date") or {}
        year = (pub_date.get("year") or {}).get("value")
        journal = summary.get("journal-title")
        doi = extract_doi(summary.get("external-ids"))
        orcid_path = summary.get("path")

        works.append({
            "title": title.strip(),
            "year": int(year) if year and str(year).isdigit() else None,
            "journal": journal.get("value").strip() if journal else None,
            "doi": doi.strip() if doi else None,
            "orcid_fallback_url": f"https://orcid.org{orcid_path}" if orcid_path else None,
        })

    print(f"  Found {len(works)} works")
    return works


def dedupe_by_doi_or_title(all_works):
    seen = {}
    order = []
    for work in all_works:
        key = (work["doi"] or "").lower() or work["title"].lower()
        if key not in seen:
            seen[key] = work
            order.append(key)
    return [seen[k] for k in order]


# ---------------------------------------------------------------------------
# Crossref: enrich with full author list, journal, volume/issue/pages
# ---------------------------------------------------------------------------

def initials_from_given_name(given_name):
    """'Jean-Paul' -> 'J.-P.'   'Jane' -> 'J.'"""
    if not given_name:
        return ""
    parts = re.split(r"(-)", given_name.strip())  # keep hyphens as separators
    out = []
    for part in parts:
        if part == "-":
            out.append("-")
        elif part:
            out.append(part[0].upper() + ".")
    return "".join(out)


def extract_authors(crossref_authors):
    """All authors on the paper (lab members and outside collaborators
    alike), formatted as 'Family, Initials'. Organizations/collaborations
    without a family name are skipped."""
    names = []
    for a in crossref_authors or []:
        family = a.get("family")
        if not family:
            continue
        initials = initials_from_given_name(a.get("given", ""))
        display = f"{family}, {initials}".strip().rstrip(",")
        names.append({"name": display})
    return names


def fetch_crossref_metadata(doi, contact_email):
    headers = {"Accept": "application/json"}
    if contact_email:
        headers["User-Agent"] = f"LabPublicationsBot/1.0 (mailto:{contact_email})"
    url = f"{CROSSREF_API_BASE}/{doi}"
    data = api_get(url, headers)
    if not data or "message" not in data:
        return None
    return data["message"]


def extract_metadata(crossref_msg, fallback_journal, fallback_year):
    """Pulls structured fields (authors, year, journal, volume, issue,
    pages) out of a Crossref work record, falling back to whatever ORCID
    already gave us where Crossref doesn't have it."""
    authors = extract_authors(crossref_msg.get("author") if crossref_msg else None)

    year = fallback_year
    if crossref_msg:
        date_parts = (
            crossref_msg.get("published-print", {}).get("date-parts")
            or crossref_msg.get("published-online", {}).get("date-parts")
            or crossref_msg.get("published", {}).get("date-parts")
        )
        if date_parts and date_parts[0]:
            year = date_parts[0][0]

    journal = fallback_journal
    if crossref_msg and crossref_msg.get("container-title"):
        journal = crossref_msg["container-title"][0]

    volume = crossref_msg.get("volume") if crossref_msg else None
    issue = crossref_msg.get("issue") if crossref_msg else None
    pages = crossref_msg.get("page") if crossref_msg else None

    return {
        "authors": authors,
        "year": year,
        "journal": journal,
        "volume": volume,
        "issue": issue,
        "pages": pages,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_lab_config():
    if not AUTHORS_FILE.exists():
        print(f"ERROR: {AUTHORS_FILE} not found.", file=sys.stderr)
        sys.exit(1)
    with open(AUTHORS_FILE) as f:
        config = yaml.safe_load(f) or {}
    authors = config.get("authors", [])
    if not authors:
        print("ERROR: no authors listed in authors.yml", file=sys.stderr)
        sys.exit(1)
    contact_email = config.get("contact_email")
    return authors, contact_email


def main():
    authors_cfg, contact_email = load_lab_config()

    all_works = []
    for author in authors_cfg:
        orcid_id = author.get("orcid")
        name = author.get("name", orcid_id)
        if not orcid_id:
            print(f"Skipping entry with no ORCID iD: {author}", file=sys.stderr)
            continue
        all_works.extend(fetch_author_works(orcid_id, name))

    if not all_works:
        print("ERROR: no works fetched for any author; aborting without overwriting output.", file=sys.stderr)
        sys.exit(1)

    deduped = dedupe_by_doi_or_title(all_works)

    current_year = datetime.date.today().year
    cutoff_year = current_year - YEARS_TO_KEEP

    print(f"\nEnriching {len(deduped)} unique works via Crossref (keeping {cutoff_year}-{current_year})...")

    publications = []
    for work in deduped:
        # Quick pre-filter on ORCID's own year if we already know it's too old,
        # to avoid unnecessary Crossref calls (final filter happens after
        # enrichment, since Crossref's year can differ slightly).
        if work["year"] and work["year"] < cutoff_year - 1:
            continue

        crossref_msg = fetch_crossref_metadata(work["doi"], contact_email) if work["doi"] else None
        meta = extract_metadata(crossref_msg, work["journal"], work["year"])

        if not meta["year"] or meta["year"] < cutoff_year:
            continue

        title = work["title"]
        if crossref_msg and crossref_msg.get("title"):
            title = crossref_msg["title"][0]

        url = f"https://doi.org/{work['doi']}" if work["doi"] else work["orcid_fallback_url"]

        publications.append({
            "title": title,
            "year": meta["year"],
            "authors": meta["authors"],
            "journal": meta["journal"],
            "volume": meta["volume"],
            "issue": meta["issue"],
            "pages": meta["pages"],
            "doi": work["doi"],
            "url": url,
        })

        time.sleep(0.1)  # be polite to Crossref

    if not publications:
        print("WARNING: no publications remained after filtering to the last "
              f"{YEARS_TO_KEEP} years. Writing an empty list.", file=sys.stderr)

    publications.sort(key=lambda p: (-(p["year"] or 0), p["title"]))

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        yaml.dump(publications, f, sort_keys=False, allow_unicode=True, width=1000)

    print(f"\nWrote {len(publications)} publications (last {YEARS_TO_KEEP} years) to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()