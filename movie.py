
# Version 2 with subfunctions for each menu-point, if you like

import random
import statistics
# import matplotlib.pyplot as plt
import movie_API
import sqlite3


# all functions for menu-selection
def goodbye():
    """leave program"""
    print("Bye!")


"""def list_movie(movies):
    #list of all movies
    print(f"{len(movies)} movies in total:")
    for title, info in movies.items():
        print(f"{title}: {info['rating']} ({info['year']})")"""

def list_movies_from_db(db_filename="movies.db"):
    """Listet alle Filme aus der Datenbank"""
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    cur.execute("SELECT title, year, rating FROM movies")
    rows = cur.fetchall()
    conn.close()

    print(f"{len(rows)} movies in total:")
    for title, year, rating in rows:
        print(f"{title}: {rating} ({year})")

def add_movie(movies):
    """add a new movie (name, rating, year)"""
    title = input("Enter a movie title (or 'q' to quit): ")
    if title.lower() == "q":
        return
    if title in movies:
        print("Movie already exists.")
        return


    # connection to database
    conn = movie_API.init_db("movies.db")

    # gets movie from db
    movie = movie_API.fetch_movie_from_omdb(film=title)
    if movie is None:
        print(f"Movie '{title}' not found in OMDb.")
        return

    # try to write film in SQL
    try:
        movie_API.add_movie_sql(conn, movie)
        print("Movie added!")
    finally:
        conn.close()

def delete_movie(movies):
    """delete a movie by name"""
    film = input("Enter the movie to delete: ")
    if film in movies:
        del movies[film]
        print(f"{film} has been deleted.")
    else:
        print("Movie not found.")


def update_movie(movies):
    """actualize a movie (rating)"""
    film = input("Enter the movie to update: ")
    if film in movies:
        new_rating = float(input("Enter the new rating: "))
        movies[film]["rating"] = new_rating
        print(f"{film} was updated to rating {new_rating}.")
    else:
        print("Movie not found.")


def stats(movies):
    """overview of statistics"""
    ratings = [info["rating"] for info in movies.values()]

    avg_rating = sum(ratings) / len(ratings)
    median_rating = statistics.median(ratings)
    max_rating = max(ratings)
    min_rating = min(ratings)
    best_movies = [m for m, i in movies.items() if i["rating"] == max_rating]
    worst_movies = [m for m, i in movies.items() if i["rating"] == min_rating]

    print(f"Total movies: {len(movies)}")
    print(f"Average rating: {avg_rating:.2f}")
    print(f"Median rating: {median_rating:.2f}")
    print(f"Best movies: {', '.join(best_movies)} ({max_rating})")
    print(f"Worst movies: {', '.join(worst_movies)} ({min_rating})")


def random_movie(movies):
    """select a film randomized"""
    film = random.choice(list(movies.keys()))
    info = movies[film]
    print(f"Random movie: {film} ({info['year']}), Rating: {info['rating']}")


def search_movie(movies):
    """find if a movie is in the dictionary"""
    search = input("Enter search term: ").lower()
    found = False
    for title, info in movies.items():
        if search in title.lower():
            print(f"{title}: {info['rating']} ({info['year']})")
            found = True
    if not found:
        print("No matches found.")

def sort_movies(movies):
    """list movies by rate descending"""
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
    print("Movies sorted by rating:")
    for title, info in sorted_movies:
        print(f"{title}: {info['rating']} ({info['year']})")

def generate_website():
    """generate website"""

    data = { 'title': 'Masterschool MovieDB'}
    with open("template.html", "r", encoding="utf-8") as f:
        template = f.read()

    html_output = template.format(**data)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_output)

    print("website was generated successfully.")


# at the moment not active because installation of matplotlib did not work properly
#"""def histogram(movies):):
 #               data = [info["rating"] for info in movies.values()]
  #              plt.hist(data, bins=4, color='pink', edgecolor='yellow')
   #             plt.xlabel('Rating')
    #            plt.ylabel('Frequency')
     #           plt.title('Movie Ratings')
      #          plt.show()
       #         plt.savefig("myplot.png")
        #        print("Histogram saved as myplot.png")

         #   else:
          #      print("Invalid choice. Try again.")"""


# here main-function starts
def main():
    """Shows menu, asks for choice, and performs actions."""
    print("***** My Movie Database *****")

# data
    movies = {
        "The Shawshank Redemption": {"rating": 9.3, "year": 1994},
        "Pulp Fiction": {"rating": 8.9, "year": 1994},
        "The Room": {"rating": 3.7, "year": 2003},
        "The Godfather": {"rating": 9.2, "year": 1972},
        "The Godfather: Part II": {"rating": 9.0, "year": 1974},
        "The Dark Knight": {"rating": 9.0, "year": 2008},
        "12 Angry Men": {"rating": 9.0, "year": 1957},
        "Everything Everywhere All At Once": {"rating": 8.0, "year": 2022},
        "Forrest Gump": {"rating": 8.8, "year": 1994},
        "Star Wars: Episode V – The Empire Strikes Back": {"rating": 8.7, "year": 1980}
    }


    while True:
        menu = """
        0. Exit
        1. List movies
        2. Add movie
        3. Delete movie
        4. Update movie
        5. Stats
        6. Random movie
        7. Search movie
        8. Movies sorted by rating
        9. Create rating histogram
        10. Generate website
        """
        print(menu)

        choice = input("Enter choice (0–9): ")

        if choice == "0":
            goodbye()
            break

        if choice == "1":
            """list_movie(movies)"""
            list_movies_from_db(db_filename="movies.db")

        elif choice == "2":
            add_movie(movies)

        elif choice == "3":
            delete_movie(movies)

        elif choice == "4":
            update_movie(movies)

        elif choice == "5":
            stats(movies)

        elif choice == "6":
            random_movie(movies)

        elif choice == "7":
            search_movie(movies)


        elif choice == "8":
            sort_movies(movies)


        # elif choice == "9":
        #   histogram(movies)

        elif choice == "10":
            generate_website()


if __name__ == "__main__":
    main()
