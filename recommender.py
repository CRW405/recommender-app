import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, request, render_template, request

app = Flask(__name__)

# client credentials
client_id = ""
client_secret = ""

# set up spotify object with client credentials
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(client_id, client_secret))


@app.route("/")
def index():
    # flask index route
    return render_template("recommender.html")


class Song:  # class to store song information
    def __init__(self, name, artists, cover, genres, uri):
        self.name = name
        self.artists = artists
        self.cover = cover
        self.genres = genres
        self.uri = uri


@app.route("/recommend", methods=["POST"])  # this is a route for an input form
def recommend():
    """Get song recommendations based on a seed song and render them in the recommender.html template.

    The seed song is obtained from the form data submitted in a POST request. The Spotify API is used to get
    recommendations based on the seed song. Each recommended song is stored as a Song object, and all Song objects
    are passed to the recommender.html template.

    Returns:
        A rendered recommender.html template with the recommended songs and a flag indicating whether any songs exist.
    """
    seed_url = request.form["seed"]  # request the seed url from the form
    try:
        # https://open.spotify.com/track/77Zm1VR4gVmpUL9n7QOcmD?si=84f34c4516724abb ## this is just a sample seed url: Loosie by Earl Sweatshirt
        # this is to get the song id from the url by splitting the url from /track/ and ?
        seed = seed_url.split("/track/")[-1].split("?")[0]

        # API call to get recommendations based on seed
        rec = sp.recommendations(seed_tracks=[seed])

        rec_songs = []
        # loop through the recommendations and get the song name, artist, cover, genres and uri
        for track in rec["tracks"]:
            artists = [artist["name"]
                       for artist in track["artists"]]  # gets list of artists
            genres = []

            # get the genres of each artist in artist list
            for artist in track["artists"]:
                artist_info = sp.artist(artist["id"])
                genres.extend(artist_info["genres"])

            song = Song(track["name"],  # this creates a song object with the song name, artist, cover, genres and uri
                        artists, track["album"]["images"][0]["url"],
                        genres,
                        track["uri"])
            rec_songs.append(song)
            songsexist = True  # this is to check if the song exists so that we know if to display songs or not, prevents errors
    except:  # if there is an error, set songsexist to false and clear rec_songs list
        songsexist = False
        rec_songs = []

    # render recommender.html and pass the rec_songs and songs exist into jinja
    return render_template("recommender.html", songs=rec_songs, songsexist=songsexist)


if __name__ == "__main__":
    app.run(debug=True)  # run the app in debug mode
