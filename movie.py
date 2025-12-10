
# Version 2 with subfunctions for each menu-point, if you like

import random
import statistics
# import matplotlib.pyplot as plt
import movie_API
import sqlite3
import movie_storage_sql
from movie_storage_sql import Movie, session

# all functions for menu-selection
def goodbye():
    """leave program"""
    print("Bye!")


def list_movies_from_db():
    """Listet alle Filme aus der SQL-Datenbank über movie_storage_sql"""
    movies = movie_storage_sql.list_movies()

    print(f"{len(movies)} movies in total:")
    for title, info in movies.items():
        year = info.get("year", "N/A")
        rating = info.get("rating", "N/A")
        print(f"{title}: {rating} ({year})")

def add_movie():
    title = input("Enter a movie title (or 'q' to quit): ")
    if title.lower() == "q":
        return

    movie = movie_API.fetch_movie_from_omdb(title)
    if not movie:
        print(f"Movie '{title}' not found.")
        return

    year = movie["year"]
    rating = movie["rating"]
    poster = movie.get("poster", "")

    try:
        movie_storage_sql.add_movie(title, year, rating, poster)
        print("Movie added to database!")
    except Exception as e:
        print(f"Error adding movie: {e}")



def delete_movie():
    """delete a movie by name"""
    film = input("Enter the movie to delete: ").strip()
    if not film:
        print("You must enter a movie title.")
        return

    movie_storage_sql.delete_movie(title=film)


def update_movie():
    """actualize a movie (rating)"""
    title = input("Enter movie title to update: ").strip()
    if not title:
        print("You must enter a movie title.")
        return

    try:
        rating = float(input("Enter new rating: "))
    except ValueError:
        print("Rating must be a number.")
        return

    movie_storage_sql.update_movie(title, rating)


def stats():
    """overview of statistics"""
    movies = movie_storage_sql.list_movies()
    if not movies:
        print("No movies found in database.")
        return

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


def random_movie():
    """select a film randomized"""
    movies = movie_storage_sql.list_movies()
    film = random.choice(list(movies.keys()))
    info = movies[film]
    print(f"Random movie: {film} ({info['year']}), Rating: {info['rating']}")


def search_movie(movies):
    """find if a movie is in the dictionary"""
    search = input("Enter search term: ").lower().strip()
    if not search:
        print("You must enter a search term.")
        return
    movies = movie_storage_sql.list_movies()
    found = False

    for title, info in movies.items():
        if search.lower() in title.lower():
            print(f"{title}: {info['rating']} ({info['year']})")
            found = True

    if not found:
        print(f"Movie '{search}' not found in OMDb.")


def sort_movies(movies):
    """list movies by rate descending"""
    movies = movie_storage_sql.list_movies()
    if not movies:
        print("No movies found in database.")
        return

    sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
    print("Movies sorted by rating:")
    for title, info in sorted_movies:
        print(f"{title}: {info['rating']} ({info['year']})")

def make_movie_grid(movies):
    """Erstellt HTML für alle Filme inkl. Poster"""
    html = ""
    for title, info in movies.items():
        poster = info.get("poster", "")  # Poster aus dem Dictionary
        year = info.get("year", "N/A")
        rating = info.get("rating", "N/A")
        html += f"""
        <li class="movie-item">
            <img src="{poster}" alt="{title}" class="movie-poster">
            <h3>{title}</h3>
            <p>Rating: {rating} ({year})</p>
        </li>
        """
    return html


def generate_website():
    """Generate a website showing all movies with posters, year, and rating."""

    movies = movie_storage_sql.list_movies()

    if not movies:
        print("No movies found in database.")
        return

    try:
        with open("template.html", "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        print("Template file 'template.html' not found.")
        return

    #creates html for all movies
    grid_html = make_movie_grid(movies)
    #creating html-list for all movies
    movies_html = ""
    for title, info in movies.items():
        poster_url = info.get("poster_url", "")
        movies_html += f"""
        <li class="cards__item">
            <div class="card__title">{title} ({info['year']})</div>
            <img src="{poster_url}" alt="{title} Poster" width="200">
            <p class="card__text">
                <strong>Rating:</strong> {info['rating']}
            </p>
        </li>
        """

    # for variable in template:
    html_output = template.replace("__TEMPLATE_MOVIE_GRID__", grid_html)

    # writing into index
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_output)

    print("Website was generated successfully.")



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
            list_movies_from_db()

        elif choice == "2":
            add_movie()

        elif choice == "3":
            delete_movie()

        elif choice == "4":
            update_movie()

        elif choice == "5":
            stats()

        elif choice == "6":
            random_movie()

        elif choice == "7":
            search_movie()


        elif choice == "8":
            sort_movies()


        # elif choice == "9":
        #   histogram(movies)

        elif choice == "10":
            generate_website()


if __name__ == "__main__":
    main()
