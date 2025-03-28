#Movie Subscriptions Database
import requests
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
api_key = "26801fdfe408ff6f3d4177c1809a99ad"
base_url = "https://api.themoviedb.org/3"

class Movie(db.Model):
    _tablename_ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    rating = db.Column(db.String, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    def __init__(self,title,genre,rating,release_year):
        self.title=title
        self.genre=genre
        self.rating=rating
        self.release_year=release_year

def add_movie(title, genre, rating, release_year):
    db.session.add(Movie(title=title, genre=genre, rating=rating, release_year=release_year))
    db.session.commit()

def search_movie(title):
    search_url = f"{base_url}/search/movie"
    params = {"api_key": api_key, "query": title}
    response = requests.get(search_url, params=params).json()

    if response["results"]:
        movie = response["results"][0]
        movie_id = movie["id"]
        movie_title = movie["title"]
        movie_genre = movie.get("genre_ids",[])
        movie_rating = movie.get("vote_average","N/A")
        release_year = movie.get("release_year","Unknown")

        print(f"\nMovie found: {movie_title} ({release_year})")
        get_streaming_providers(movie_id)
    else:
        print("\nMovie not found")

def get_streaming_providers(movie_id):
    providers_url = f"{base_url}/movie/{movie_id}/watch/providers"
    params = {"api_key": api_key}
    response = requests.get(providers_url, params=params).json()

    if "results" in response and "US" in response["results"]:
        providers = response["results"]["US"].get("flatrate",[])
        if providers:
            streaming_services = [p["provider_name"] for p in providers]
            print("Available on:", ", ".join(streaming_services))
        else:
            print("Movie not available for streaming")
    else:
        print("Movie not available for streaming")

movie_name = input("Enter a movie title:")
search_movie(movie_name)
