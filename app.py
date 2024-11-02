from flask import Flask, request, render_template
import requests
import pickle

app = Flask(__name__)

# Load movie data and similarity matrix
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=390e76286265f7638bb6b19d86474639&language=en-US"
    data = requests.get(url).json()
    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}" if 'poster_path' in data else None

# Function to get recommended movies
def get_recommendations(movie):
    idx = movies[movies['title'] == movie].index[0]
    sim_scores = sorted(list(enumerate(similarity[idx])), key=lambda x: x[1], reverse=True)[1:6]
    movie_indices = [i[0] for i in sim_scores]
    movie_titles = movies['title'].iloc[movie_indices].tolist()
    movie_posters = [fetch_poster(movies['movie_id'].iloc[i]) for i in movie_indices]
    return movie_titles, movie_posters

# Main page route
@app.route('/', methods=['GET', 'POST'])
def index():
    movie_list = movies['title'].tolist()
    if request.method == 'POST':
        movie_title = request.form['selected_movie']
        recommended_movie_titles, recommended_movie_posters = get_recommendations(movie_title)
        return render_template('index.html', movie_list=movie_list,
                               recommended_movie_titles=recommended_movie_titles,
                               recommended_movie_posters=recommended_movie_posters)
    return render_template('index.html', movie_list=movie_list)

if __name__ == '__main__':
    app.run(debug=True)
