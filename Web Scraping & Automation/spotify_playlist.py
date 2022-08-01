# Importing relevant modules/libraries
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Declaring constants and global variables
QUERY_SCOPE = "playlist-modify-private"
CACHE_PATH = "token.txt"
REDIRECT_URL = "http://example.com"
SPOTIFY_ID = "6664757bb5a84c0aaf93e314f2db9b63"
SPOTIFY_SECRET = "9cb2fe88028a4242abd82d081178fbde"
AUTH_TOKEN = "BQClu4nAb_5wlJW0XO7Mny_jxj7c7fuK2E-8cYQ8mGizAS4MHMVA5191FGh7W86_AJMbOPlfjxRIU4ldIV3ZJmhdhEDH7s_KFboGJ-QPNvBAMZNz63nuca_a8SB0lep3rjm3hU0guMk5LhP3j8Y2RvVcszT9c6XTj5AWnSwlDAVsjOQqRiS3cw9uwMtT52DpGEmJN3BkmW18UbuQ2w"
billboard_url = "https://www.billboard.com/charts/hot-100/{}/"


# Determining whether or not the given date is valid
def validate_date(date: str) -> bool:

    is_valid = True

    # Invalid date - entry is missing/has extra characters, or missing the two hyphens required to properly separate the segments
    if date[4] != '-' or date[7] != '-' or len(date) != 10:

        is_valid = False

    sequences = date.split('-')
    valid_ranges = [(1960, 2022), (1, 13), (1, 29)]
    seq_index = 0

    for sequence in sequences:

        # Invalid date - one of the segments is not numerical
        if not sequence.isdigit():

            is_valid = False

        else:

            # Invalid date - one of the segments remains outside of its accepted range
            if int(sequence) not in range(valid_ranges[seq_index][0], valid_ranges[seq_index][1]):

                is_valid = False

        seq_index += 1

    return is_valid


# Returns a list containing the songs present on the Billboard Hot 100 Chart on the given date
def get_top_100(date: str) -> list:

    response = requests.get(billboard_url.format(date))
    soup = BeautifulSoup(response.text, "lxml")

    # Extracting the song names from the webpage (using the Beautiful Soup web-scraping library)
    all_songs = soup.find_all("h3", id="title-of-a-story", class_="a-no-trucate")
    top_100 = []

    for song in all_songs:

        top_100.append(song.text.strip())

    return top_100


# Returns a tuple containing the Spotify API Client, and the ID associated with the user's account
def get_user_id() -> tuple:

    # Spotify authentication (via OAuth), providing access to the desired account
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_ID,
            client_secret=SPOTIFY_SECRET,
            scope=QUERY_SCOPE,
            redirect_uri=REDIRECT_URL,
            cache_path=CACHE_PATH
        ),
        auth=AUTH_TOKEN
    )

    return sp, sp.current_user()["id"]


# Returns a list containing the Spotify URIs corresponding to the song/track names
def get_song_uris(spotify_client, date: str, song_names: list) -> list:

    year = date.split('-')[0]
    song_uris = []

    for song in song_names:

        result = spotify_client.search(q="track:{} year:{}".format(song, year), type="track")

        try:

            uri = result["tracks"]["items"][0]["uri"]

        # The song is not found in the spotify catalogue (according to the failed query), and thus it is skipped over
        except (ValueError, TypeError, KeyError, IndexError):

            continue

        song_uris.append(uri)

    return song_uris


# Constructing the Spotify playlist
def generate_playlist(spotify_client, date: str, user_id: str, song_uris: list):

    # Specifying a title and description for the new playlist
    title = "{} Billboard Top 100".format(date)
    description = "A playlist containing the Billboard Hot 100 Songs from {} * Note: Songs not present in the spotify catalogue have been omitted".format(date)

    # Creating a new private playlist (initially empty)
    new_playlist = spotify_client.user_playlist_create(
        user=user_id,
        name=title,
        public=False,
        collaborative=False,
        description=description
    )

    # Populating the newly created playlist with the given song URIs
    spotify_client.user_playlist_add_tracks(
        user=user_id,
        playlist_id=new_playlist["id"],
        tracks=song_uris,
        position=None
    )


if __name__ == "__main__":

    # Displaying the welcome message, and prompting the user to enter a date
    print("Welcome to the Musical Time Machine! (Sponsored by Billboard Hot 100 & Spotify)")
    user_date = input("What date would you like to travel to? Please enter a date in the YYYY-MM-DD format: ")

    # Continually prompting the user until a valid date is entered
    while not validate_date(user_date):

        user_date = input("Invalid selection - please enter a date in the YYYY-MM-DD format: ")
        validate_date(user_date)

    # Constructing a Spotify playlist containing the top 100 songs from the specified date (via the Billboard Hot 100 Chart)
    songs = get_top_100(user_date)
    client, user_id = get_user_id()
    song_uris = get_song_uris(client, user_date, songs)
    generate_playlist(client, user_date, user_id, song_uris)
