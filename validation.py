import re

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
