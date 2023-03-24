import openai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, render_template, request


#authentication stuff
openai.api_key = "YOUR_KEY_HERE"

spotify_client_id = "YOUR_ID_HERE"
spotify_client_secret = "YOUR_SECRET_HERE"

spotify_client_credentials_manager = SpotifyClientCredentials(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret
)
spotify = spotipy.Spotify(
    client_credentials_manager=spotify_client_credentials_manager
)

#Flask setup
app = Flask(__name__)

#Uses OpenAI to generate tags for a song that user inputs, with DaVinci 3 engine
def get_song_tags(song_title):
    prompt = f"Generate 5-7 one word tags (separated by commas) for this song that are in lowercase. Do not include anything else except the letters.'{song_title}'."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    tags = response.choices[0].text.strip()
    return tags

#Uses OpenAI to make a playlist of songs that match the tags
def generate_playlist(tags):
    prompt=f"Generate a playlist of 10, real songs, that match these tags: '{tags}'"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    playlist = response.choices[0].text.strip()
    return playlist

#renders the web page
@app.route("/")
def home():
    return render_template("index.html")

#returns the playlist
@app.route("/song", methods=["POST","GET"])
def get_input():
    formattedPlaylist = ""
    real_songs = []
    song = request.form["song"]
    tags = get_song_tags(song)
    playlist = generate_playlist(tags)

    for song in playlist.split("\n"):
        result = spotify.search(q=song, type="track", limit=1)
        if len(result["tracks"]["items"]) > 0:
            track_id = result["tracks"]["items"][0]["id"]
            track_url = result["tracks"]["items"][0]["external_urls"]["spotify"]
            real_songs.append(result["tracks"]["items"][0]["name"] + " \n" + track_url)

    if len(real_songs) > 0:
        formattedPlaylist += "Here's your playlist:\n"
        for song1 in real_songs:
            formattedPlaylist+= f"- {song1}\n"

    return formattedPlaylist

if __name__ == '__main__':
    app.run()



#console version
print("Welcome to SpotifAI.");
#Asks user to put in their favorite song, generates tags and then uses the tags to generate a playlist
song = input("Input a song to get started: ")
tags = get_song_tags(song)
print(f"Here are some tags for the song '{song}': {tags}")
playlist = generate_playlist(tags)

#Uses spotify to check if the songs that were generated were real and not just made up by the AI.
#Gets the full name of the song and a playable link.
real_songs = []

for song in playlist.split("\n"):
    result = spotify.search(q=song, type="track", limit=1)
    if len(result["tracks"]["items"]) > 0:
        track_id = result["tracks"]["items"][0]["id"]
        track_url = result["tracks"]["items"][0]["external_urls"]["spotify"]
        real_songs.append(result["tracks"]["items"][0]["name"] + " \n" + track_url)

if len(real_songs) > 0:
    print("Here's your playlist:")
    for song in real_songs:
        print(f"- {song}")
else:
    print("")