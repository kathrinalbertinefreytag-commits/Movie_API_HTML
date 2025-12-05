import movie_API

def make_movie_grid(movies):
    html = ""
    for movie in movies:
        html += f"""
        <li class="movie-item">
            <img src="{movie['poster']}" alt="{movie['title']}" class="movie-poster">
            <h3>{movie['title']}</h3>
            <p>Rating: {movie['rating']}</p>
        </li>
        """
    return html

# --- Collect movies from API ---
titles = ["Titanic", "The english Patient", "Moonlight"]

movies = []
for title in titles:
    movie = movie_API.fetch_movie_from_omdb(title)
    if movie:
        movies.append(movie)


with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()


grid_html = make_movie_grid(movies)

full_html = template.replace("__TEMPLATE_MOVIE_GRID__", grid_html)

# --- Save result ---
with open("index.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("Website generated → index.html created!")
