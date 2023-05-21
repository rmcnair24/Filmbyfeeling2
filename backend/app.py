from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
import os
from flask_cors import CORS

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'frontend/public'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'movies.db')
db = SQLAlchemy(app)

# Enable CORS
CORS(app)

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '../frontend/public'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'movies.db')
db = SQLAlchemy(app)


# Define the Movie model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    release_year = db.Column(db.Integer)


def populate_database():
    movies = [
        {'title': 'Airplane!', 'genre': 'Happy', 'release_year': 1980},
        # Rest of the movie data
        # ...
    ]

    for movie_data in movies:
        movie = Movie(
            title=movie_data['title'],
            genre=movie_data['genre'],
            release_year=movie_data['release_year']
        )
        db.session.add(movie)

    db.session.commit()


# Define routes
@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/search', methods=['POST'])
def search():
    emotion = request.form['emotion']
    birth_year = int(request.form['birth_year'])

    # Calculate the date range
    min_year = birth_year + 10
    max_year = birth_year + 35

    # Query the movies
    movies = Movie.query.filter(Movie.genre == emotion,
                                Movie.release_year >= min_year,
                                Movie.release_year <= max_year).all()

    if len(movies) >= 3:
        # Randomly select 3 movies
        selected_movies = random.sample(movies, 3)
    else:
        # Handle the case where there are fewer than 3 movies
        selected_movies = movies

    return render_template('results.html', movies=selected_movies)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        populate_database()

    app.run(port=3001)