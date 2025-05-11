#Movie Subscriptions Database
import requests
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy()
db.init_app(app)
api_key = "26801fdfe408ff6f3d4177c1809a99ad"
base_url = "https://api.themoviedb.org/3"

class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    rating = db.Column(db.String, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "title": self.title,
            "genre": self.genre,
            "rating": self.rating,
            "release_year": self.release_year
        }

with app.app_context():
    db.create_all()

def get_mpaa_rating(movie_id):
    url = f"{base_url}/movie/{movie_id}/release_dates"
    params = {"api_key": api_key}
    response = requests.get(url, params=params).json()

    for result in response.get("results", []):
        if result["iso_3166_1"] == "US":
            for release in result["release_dates"]:
                cert = release.get("certification")
                if cert:
                    return cert
    return "Not Rated"
@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search' , methods=['GET'])
def search_movie():
    title = request.args.get('title')
    if not title:
        return render_template('search.html' , error= "Please enter a movie title."), 400
    
    search_url = f"{base_url}/search/movie"
    params = {"api_key": api_key, "query": title}

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500 

    if data["results"]:
        movie = data["results"][0]
        movie_id = movie["id"]
        movie_title = movie["title"]
        movie_genre = movie.get("genre_ids",[])
        movie_rating = get_mpaa_rating(movie_id)
        release_date = movie.get("release_date","")
        release_year = release_date.split("-")[0] if release_date else "Unknown"

        genres = get_genre_names(movie_genre)
        providers = get_streaming_providers(movie_id)

        new_movie = Movie(title=movie_title, genre=genres, rating=str(movie_rating), release_year=release_year)
        db.session.add(new_movie)
        db.session.commit()

        return render_template('search.html', results={
            "title": movie_title,
            "genre": genres,
            "rating": movie_rating,
            "release_year": release_year,
            "streaming_providers": providers
        })
    else:
        return render_template('search.html', error="Movie not found.")

def get_genre_names(genre_ids):
    genre_url= f"{base_url}/genre/movie/list"
    params = {"api_key": api_key}
    response = requests.get(genre_url, params=params).json()
    genre_map = {g["id"]: g["name"] for g in response["genres"]}
    return ", ".join([genre_map.get(gid, "Unknown") for gid in genre_ids])

def get_streaming_providers(movie_id):
    providers_url = f"{base_url}/movie/{movie_id}/watch/providers"
    params = {"api_key": api_key}
    response = requests.get(providers_url, params=params).json()

    if "results" in response and "US" in response["results"]:
        providers = response["results"]["US"].get("flatrate", [])
        return [p["provider_name"] for p in providers]
    return []

if __name__ == "__main__":
    app.run(debug=True)
