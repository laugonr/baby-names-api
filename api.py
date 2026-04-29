from datetime import datetime
from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from database import create_table, get_connection
from validation import validate_gender, validate_name

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Baby Names API",
    version="Development",
    description="Search baby name popularity data by year.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

create_table()


@app.get("/")
def home():
    return {
        "message": "Baby Names API is running!",
        "version": "Development",
        "endpoints": {
            "GET /": "API information",
            "GET /app": "Baby name analyzer web app",
            "GET /nameinfo?name=<name>&gender=<M|F>": "Get name statistics",
            "GET /docs": "Interactive API docs",
        },
    }


@app.get("/app")
def frontend():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/nameinfo")
def name_info(
    name: str = Query(..., description="Name to search for"),
    gender: str = Query(..., description="Gender to search for: M or F"),
):
    try:
        validated_name = validate_name(
            name,
            message="Name parameter is required",
        )
        validated_gender = validate_gender(gender)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    try:
        with get_connection() as conn:
            yearly_totals = conn.execute("""
                SELECT year, SUM(count) AS total_count
                FROM baby_names
                WHERE name = ? AND gender = ?
                GROUP BY year
                ORDER BY year ASC
            """, (validated_name, validated_gender)).fetchall()

    except sqlite3.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}",
        ) from e

    if not yearly_totals:
        raise HTTPException(
            status_code=404,
            detail={
                "error": f"Name '{validated_name}' not found in database",
                "name": validated_name,
                "gender": validated_gender,
                "available": False,
            },
        )

    first_year = yearly_totals[0][0]
    most_popular_year = max(yearly_totals, key=lambda row: row[1])[0]
    top_years = [
        year for year, _ in sorted(
            yearly_totals,
            key=lambda row: row[1],
            reverse=True,
        )[:10]
    ]
    yearly_data = [
        {"year": year, "count": total_count}
        for year, total_count in yearly_totals
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

    return {
        "name": validated_name,
        "gender": validated_gender,
        "first_year": first_year,
        "most_popular_year": most_popular_year,
        "top_years": top_years,
        "yearly_data": yearly_data,
        "estimated_age": estimated_age,
        "trend": trend,
        "available": True,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
