from sqlalchemy import create_engine, Column, Integer, String, Float, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()
DB_URL = "sqlite:///movies.db"
engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    year = Column(Integer)
    rating = Column(Float)
    poster = Column(String)  # die Spalte für Poster

# creates Table if not existing
Base.metadata.create_all(engine)

# checking, if Poster exists, adding poster
inspector = inspect(engine)
columns = [col["name"] for col in inspector.get_columns("movies")]
if "poster" not in columns:
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE movies ADD COLUMN poster TEXT"))
        conn.commit()
    print("Poster column added to movies table")


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies}


def add_movie(title, year, rating, poster=""):
    movie = Movie(title=title, year=year, rating=rating, poster=poster)
    session.add(movie)
    session.commit()


def delete_movie(title):
    """Delete a movie from the database identified by its title."""
    with engine.begin() as connection:
        result = connection.execute(text("DELETE FROM movies WHERE title = :title;"),
        {"title": title})
        if result.rowcount == 0:
            print(f"No movie found with title '{title}'.")
        else:
            print(f"{title} deleted successfully.")

def update_movie(title, rating):
    """Update the rating of a movie identified by its title."""
    with engine.begin() as connection:
        result = connection.execute(text("UPDATE movies SET rating = :rating WHERE title = :title;"),
                                    {"rating": rating, "title": title})
        if result.rowcount == 0:
            print(f"No movie found with title '{title}'.")
        else:
            print(f"{title} updated successfully.")
