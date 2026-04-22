from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import re
from database import create_table

app = Flask(__name__)

DB_NAME = "babynames.db"
create_table()


def validate_name(name):
    """Validate name parameter"""
    if not name or not name.strip():
        return None, "Name parameter is required"
    
    name = name.strip()
    
    # Check length
    if len(name) > 50:
        return None, "Name is too long (max 50 characters)"
    
    # Check for valid characters (letters, spaces, hyphens, apostrophes)
    if not re.match(r"^[a-zA-Z\s\-']+$", name):
        return None, "Name contains invalid characters"
    
    return name.title(), None


@app.route("/")
def home():
    return jsonify({
        "message": "Baby Names API is running!",
        "version": "Development",
        "endpoints": {
            "GET /": "API information",
            "GET /nameinfo?name=<name>": "Get name statistics"
        }
    })


@app.route("/nameinfo")
def name_info():
    # Get and validate name parameter
    name_param = request.args.get("name")
    name, error = validate_name(name_param)
    
    if error:
        return jsonify({"error": error}), 400
    
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            
            # First year (using MIN aggregate - safe)
            cursor.execute("SELECT MIN(year) FROM baby_names WHERE name = ?", (name,))
            first_year_result = cursor.fetchone()
            first_year = first_year_result[0] if first_year_result and first_year_result[0] else None
            
            # Most popular year (can return None - need to handle)
            cursor.execute("""
                SELECT year FROM baby_names
                WHERE name = ?
                ORDER BY count DESC LIMIT 1
            """, (name,))
            most_popular_result = cursor.fetchone()
            most_popular_year = most_popular_result[0] if most_popular_result else None
            
            # Top 10 years (safe - returns empty list if no data)
            cursor.execute("""
                SELECT DISTINCT year FROM baby_names
                WHERE name = ?
                ORDER BY year DESC LIMIT 10
            """, (name,))
            top_years_results = cursor.fetchall()
            top_years = [row[0] for row in top_years_results]

            cursor.execute("""
                SELECT year, SUM(count) AS total_count
                FROM baby_names
                WHERE name = ?
                GROUP BY year
                ORDER BY year ASC
            """, (name,))
            yearly_totals = cursor.fetchall()
            
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
    # Check if name exists in database
    if first_year is None:
        return jsonify({
            "error": f"Name '{name}' not found in database",
            "name": name,
            "available": False
        }), 404
    
    # Estimate age
    current_year = datetime.now().year
    estimated_age = current_year - most_popular_year if most_popular_year else None

    # Compare earliest and latest popularity totals to classify the trend.
    trend = "unknown"
    if len(yearly_totals) > 1:
        first_total = yearly_totals[0][1]
        last_total = yearly_totals[-1][1]
        if last_total > first_total:
            trend = "recent"
        elif last_total < first_total:
            trend = "older"
        else:
            trend = "stable"
    
    return jsonify({
        "name": name,
        "first_year": first_year,
        "most_popular_year": most_popular_year,
        "top_years": top_years,
        "estimated_age": estimated_age,
        "trend": trend,
        "available": True
    })


if __name__ == "__main__":
    app.run(debug=True)
