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

def fetch_movie_from_omdb(title):
    url = "http://www.omdbapi.com/"
    params = {
        "apikey": api_key,
        "t": title,
        "r": "json"
    }

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen von OMDb: {e}")
    if resp.status_code != 200:
        return None

    data = resp.json()
    if data.get("Response") == "False":
        print(f"OMDb: Film '{title}' nicht gefunden")
        return None

    # Daten von OMDb
    imdb_rating = data.get("imdbRating")
    try:
        imdb_rating = float(imdb_rating) if imdb_rating != "N/A" else None
    except (ValueError, TypeError):
        imdb_rating = None

    try:
        year = int(data.get("Year", 0))
    except (ValueError, TypeError):
        year = None

    return {
        "title": data.get("Title"),
        "year": year,
        "rating": imdb_rating,
        "poster": data.get("Poster", "")
    }

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