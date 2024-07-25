from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
import os

date = input("which date you want listen (YYYY-MM-DD): ")
url = f'https://www.billboard.com/charts/hot-100/{date}'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select('li ul li h3')
song_names = [song.getText().strip() for song in song_names_spans]


CLIENT_ID = os.environ.get("spotify_client_id")
CLIENT_SECRET = os.environ.get("spotify_client_secret")
scope = 'playlist-modify-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://example.com",
    scope=scope,
    show_dialog=True,
    cache_path="token.txt",
    username='Mustafaakgul'
))
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
        continue

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
