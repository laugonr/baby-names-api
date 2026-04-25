from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
from database import create_table, get_connection
from validation import validate_name

app = Flask(__name__)

create_table()


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
    try:
        name = validate_name(
            request.args.get("name"),
            message="Name parameter is required"
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    try:
        with get_connection() as conn:
            yearly_totals = conn.execute("""
                SELECT year, SUM(count) AS total_count
                FROM baby_names
                WHERE name = ?
                GROUP BY year
                ORDER BY year ASC
            """, (name,)).fetchall()

    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    if not yearly_totals:
        return jsonify({
            "error": f"Name '{name}' not found in database",
            "name": name,
            "available": False
        }), 404

    first_year = yearly_totals[0][0]
    most_popular_year = max(yearly_totals, key=lambda row: row[1])[0]
    top_years = [
        year for year, _ in sorted(
            yearly_totals,
            key=lambda row: row[1],
            reverse=True
        )[:10]
    ]

    current_year = datetime.now().year
    estimated_age = current_year - most_popular_year

    trend = "unknown"
    if len(yearly_totals) > 1:
        first_total = yearly_totals[0][1]
        last_total = yearly_totals[-1][1]
        if last_total > first_total:
            trend = "rising"
        elif last_total < first_total:
            trend = "declining"
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
    create_table()
    app.run(debug=True)
