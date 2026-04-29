import re
from datetime import datetime

MIN_YEAR = 1880
MAX_YEAR = datetime.now().year
NAME_PATTERN = re.compile(r"^[a-zA-Z\s\-']+$")


def validate_name(name, message="Name cannot be empty"):
    if not name or not name.strip():
        raise ValueError(message)

    name = name.strip()
    if len(name) > 50:
        raise ValueError("Name is too long (max 50 characters)")
    if not NAME_PATTERN.fullmatch(name):
        raise ValueError("Name contains invalid characters")
    return name.title()


def validate_year(year_str):
    try:
        year = int(year_str)
    except ValueError as exc:
        raise ValueError("Year must be a valid number") from exc

    if year < MIN_YEAR or year > MAX_YEAR:
        raise ValueError(f"Year must be between {MIN_YEAR} and {MAX_YEAR}")
    return year


def validate_gender(gender):
    gender = gender.strip().upper()
    if gender not in ("M", "F"):
        raise ValueError("Gender must be 'M' or 'F'")
    return gender


def validate_count(count_str):
    try:
        count = int(count_str)
    except ValueError as exc:
        raise ValueError("Count must be a valid number") from exc

    if count < 0:
        raise ValueError("Count cannot be negative")
    return count
