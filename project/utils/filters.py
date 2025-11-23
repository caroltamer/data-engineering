from pathlib import Path
import pandas as pd
from typing import Union

# ===========================
# Column constants used across the project
# ===========================
COL_BOROUGH = "BOROUGH"
COL_YEAR = "CRASH_YEAR"
COL_MONTH = "CRASH_MONTH"
COL_HOUR = "CRASH_HOUR"
COL_LAT = "LATITUDE"
COL_LON = "LONGITUDE"
COL_COLLISION_ID = "COLLISION_ID"
COL_PERSON_INJURY = "PERSON_INJURY"
COL_PERSON_TYPE = "PERSON_TYPE"
COL_VEHICLE_TYPE = "VEHICLE_TYPE_CODE_1"
COL_FACTOR = "CONTRIBUTING_FACTOR_VEHICLE_1"

# ===========================
# Path to your final CSV
# ===========================
DEFAULT_DATA_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "integrated_cleaned_final.csv"
)

# ===========================
# Optional column renames (if your CSV has spaces or different naming)
# ===========================
RENAMES = {
    "BOROUGH ": COL_BOROUGH,
    "CRASH YEAR": COL_YEAR,
    "CRASH MONTH": COL_MONTH,
    "CRASH HOUR": COL_HOUR,
    "LATITUDE ": COL_LAT,
    "LONGITUDE ": COL_LON,
    "VEHICLE TYPE CODE 1": COL_VEHICLE_TYPE,
    "CONTRIBUTING FACTOR VEHICLE 1": COL_FACTOR,
    "PERSON TYPE": COL_PERSON_TYPE,
    "PERSON INJURY": COL_PERSON_INJURY,
    "COLLISION_ID": COL_COLLISION_ID,
}

def load_data(path: Union[Path, str] = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """
    Load the cleaned CSV dataset for the dashboard.
    Performs light normalization on column names & types.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found at: {path}")

    # Load CSV
    df = pd.read_csv(path)

    # Rename any mismatched columns
    rename_map = {old: new for old, new in RENAMES.items() if old in df.columns}
    if rename_map:
        df.rename(columns=rename_map, inplace=True)

    # Ensure numeric columns are numeric
    for col in [COL_YEAR, COL_MONTH, COL_HOUR]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Clean string columns
    for col in [
        COL_BOROUGH,
        COL_PERSON_INJURY,
        COL_PERSON_TYPE,
        COL_VEHICLE_TYPE,
        COL_FACTOR,
    ]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df
# ===========================
# Search query parsing
# ===========================
def parse_search_query(query: str) -> dict:
    """
    Parse a free-text search query into structured filters.
    Example:
        'manhattan 2021 speed' ->
        {
            "borough": "MANHATTAN",
            "year": 2021,
            "keywords": ["speed"]
        }
    """
    if not query:
        return {}

    parts = query.strip().split()
    result = {
        "borough": None,
        "year": None,
        "keywords": [],
    }

    for p in parts:
        up = p.upper()
        # Try to detect borough
        if up in ["MANHATTAN", "BROOKLYN", "QUEENS", "BRONX", "STATEN", "STATEN ISLAND"]:
            result["borough"] = "STATEN ISLAND" if up.startswith("STATEN") else up
        # Try to detect a year like 2019, 2020, 2021...
        elif p.isdigit() and len(p) == 4:
            try:
                result["year"] = int(p)
            except ValueError:
                pass
        else:
            result["keywords"].append(p)

    return result


# ===========================
# Main filtering helper
# ===========================
from typing import List, Optional


def apply_filters(
    df: pd.DataFrame,
    boroughs: Optional[List[str]] = None,
    years: Optional[List[int]] = None,
    months: Optional[List[int]] = None,
    hours: Optional[List[int]] = None,
    injuries: Optional[List[str]] = None,
    person_types: Optional[List[str]] = None,
    vehicle_types: Optional[List[str]] = None,
    factors: Optional[List[str]] = None,
    search_text: Optional[str] = None,
) -> pd.DataFrame:
    """
    Generic filtering helper used by callbacks.

    All arguments are optional; if a filter is None or empty, it is ignored.
    """
    filtered = df.copy()

    # Borough filter
    if boroughs and COL_BOROUGH in filtered.columns:
        boroughs_up = [b.upper() for b in boroughs]
        filtered = filtered[filtered[COL_BOROUGH].str.upper().isin(boroughs_up)]

    # Year filter
    if years and COL_YEAR in filtered.columns:
        filtered = filtered[filtered[COL_YEAR].isin(years)]

    # Month filter
    if months and COL_MONTH in filtered.columns:
        filtered = filtered[filtered[COL_MONTH].isin(months)]

    # Hour filter
    if hours and COL_HOUR in filtered.columns:
        filtered = filtered[filtered[COL_HOUR].isin(hours)]

    # Injury filter
    if injuries and COL_PERSON_INJURY in filtered.columns:
        filtered = filtered[filtered[COL_PERSON_INJURY].isin(injuries)]

    # Person type filter
    if person_types and COL_PERSON_TYPE in filtered.columns:
        filtered = filtered[filtered[COL_PERSON_TYPE].isin(person_types)]

    # Vehicle type filter
    if vehicle_types and COL_VEHICLE_TYPE in filtered.columns:
        filtered = filtered[filtered[COL_VEHICLE_TYPE].isin(vehicle_types)]

    # Factor filter
    if factors and COL_FACTOR in filtered.columns:
        filtered = filtered[filtered[COL_FACTOR].isin(factors)]

    # Free-text search in factor / vehicle / borough
    if search_text:
        text = search_text.strip().lower()
        if text:
            mask = pd.Series(True, index=filtered.index)
            for col in [COL_FACTOR, COL_VEHICLE_TYPE, COL_BOROUGH]:
                if col in filtered.columns:
                    mask &= filtered[col].astype(str).str.lower().str.contains(text, na=False)
            filtered = filtered[mask]

    return filtered