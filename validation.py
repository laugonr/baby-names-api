import re
from datetime import datetime

# SSA baby name data starts in 1880.
MIN_YEAR = 1880

# Do not allow future years.
MAX_YEAR = datetime.now().year

# Names can contain letters, spaces, hyphens, and apostrophes.
NAME_PATTERN = re.compile(r"^[a-zA-Z\s\-']+$")


def validate_name(name, message="Name cannot be empty"):
    """Clean a name and make sure it only has allowed characters."""
    if not name or not name.strip():
        raise ValueError(message)

    name = name.strip()
    if len(name) > 50:
        raise ValueError("Name is too long (max 50 characters)")
    if not NAME_PATTERN.fullmatch(name):
        raise ValueError("Name contains invalid characters")
    return name.title()


def validate_year(year_str):
    """Make sure the year is a real number within the allowed range."""
    try:
        year = int(year_str)
    except ValueError as exc:
        raise ValueError("Year must be a valid number") from exc

    if year < MIN_YEAR or year > MAX_YEAR:
        raise ValueError(f"Year must be between {MIN_YEAR} and {MAX_YEAR}")
    return year


def validate_gender(gender):
    """Make sure gender is either M or F."""
    gender = gender.strip().upper()
    if gender not in ("M", "F"):
        raise ValueError("Gender must be 'M' or 'F'")
    return gender


def validate_count(count_str):
    """Make sure the birth count is a non-negative number."""
    try:
        count = int(count_str)
    except ValueError as exc:
        raise ValueError("Count must be a valid number") from exc

    if count < 0:
        raise ValueError("Count cannot be negative")
    return count
