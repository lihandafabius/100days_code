from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "212ed808ad8243edb1fa81560f9c6684"
CLIENT_SECRET = "4e2d412fba3b4ed7af80c59e564d63ba"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="http://example.com",
        scope="playlist-modify-private",
        show_dialog = True,
        cache_path = "token.txt",
        username="Lihanda"
       )
    )

user_id = sp.current_user()["id"]

time = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
response = requests.get("https://www.billboard.com/charts/hot-100/" + time)
data = response.text
# print(data)
bill_board_track = []
soup = BeautifulSoup(data, "html.parser")
music_list = soup.select("li ul li h3")
# print(music_list)
song_uris = []
year = time.split("-")[0]
for music in music_list:
    bill_board_track.append(music.getText().strip())

# print(bill_board_track)
for song in bill_board_track:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

user_id = sp.current_user()["id"]

playlist = sp.user_playlist_create(user=user_id, name=f"{year} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

