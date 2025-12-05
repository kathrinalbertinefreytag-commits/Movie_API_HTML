import sqlite3
import requests
from dotenv import load_dotenv
import os


load_dotenv()  # Looks for .env in current directory or parent dirs


api_key = os.getenv("API_KEY")



def init_db(db_filename="movies.db"):#.db
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER,
            imdb_rating REAL
        )
    """)
    conn.commit()
    return conn

def fetch_movie_from_omdb(film):
    url = "http://www.omdbapi.com/"
    params = {
        "apikey": api_key,
        "t": film,
        "r": "json"
    }
    resp = requests.get(url, params=params, timeout=5)
    if resp.status_code != 200:
        return None

    data = resp.json()
    if data.get("Response") == "False":
        return None  # Film nicht gefunden
    # Beispiel: Daten aus OMDb
    year = data.get("Year")
    imdb_rating = data.get("imdbRating")
    try:
        year = int(year)
    except (ValueError, TypeError):
        year = None
    try:
        imdb_rating = float(imdb_rating)
    except (ValueError, TypeError):
        imdb_rating = None
    return {"title": data.get("Title"),
            "year": int(data.get("Year", 0)),
            "rating": float(data.get("imdbRating")) if data.get("imdbRating") != "N/A" else None}

def add_movie_sql(conn, movie):
    cur = conn.cursor()
    try:
        cur.execute(""" 
            INSERT INTO movies (title, year, rating)
            VALUES (?, ?, ?)
        """, (movie["title"], movie["year"], movie["rating"]))
        conn.commit()
        print(f"Added movie: {movie['title']} ({movie['year']}) — Rating: {movie['rating']}")
    except sqlite3.IntegrityError:
        print("Movie already exists in the database.")

if __name__ == "__main__":
    conn = init_db()
    title = input("Enter a movie title (or 'q' to quit): ").strip()
    if title.lower() != "q":
        add_movie_sql(conn, title)
    else:
        conn.close()