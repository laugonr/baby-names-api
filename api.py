from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_NAME = "babynames.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

@app.route("/")
def home():
    return "Baby Names API is running!"
@app.route("/nameinfo")
def name_info():
    name = request.args.get("name")

    conn = get_connection()
    cursor = conn.cursor()

    # First year
    cursor.execute("SELECT MIN(year) FROM baby_names WHERE name = ?", (name,))
    first_year = cursor.fetchone()[0]

    # Most popular year
    cursor.execute("""
        SELECT year FROM baby_names
        WHERE name = ?
        ORDER BY count DESC LIMIT 1
    """, (name,))
    most_popular_year = cursor.fetchone()[0]

    # Top 10 years (no duplicates)
    cursor.execute("""
        SELECT DISTINCT year FROM baby_names
        WHERE name = ?
        ORDER BY count DESC LIMIT 10
    """, (name,))
    top_years = [row[0] for row in cursor.fetchall()]

    conn.close()

    # Estimate age
    estimated_age = 2026 - most_popular_year if most_popular_year else None

    # Trend logic
    trend = "unknown"
    if len(top_years) > 1:
        if top_years[0] > top_years[-1]:
            trend = "rising"
        else:
            trend = "declining"

    return jsonify({
        "name": name,
        "first_year": first_year,
        "most_popular_year": most_popular_year,
        "top_years": top_years,
        "estimated_age": estimated_age,
        "trend": trend
    })

if __name__ == "__main__":
    app.run(debug=True)