import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import schedule
import time


# Read passwords and client codes from a file
def read_file_codes():
    file = open("secret_text.txt", "r")

    lines = file.readlines()

    password_array = []

    for line in lines:
        line_split = line.split('"')[1]
        password_array.append(line_split)

    file.close()

    return password_array


# Get the top ten recommended songs from reddit and return 'title and artist' in a list
def gather_reddit_posts(reddit_client_id, reddit_client_secret, reddit_password):
    # Client data given by reddit
    client_id = reddit_client_id
    client_secret = reddit_client_secret

    # Creates a basic http authentication
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)

    # Json to hold our user data
    data = {
        'grant_type': 'password',
        'username': 'Zestyclose-Detail367',
        'password': reddit_password
    }
    headers = {'User-Agent': 'webscrape_test'}

    # Creates https post request to reddit
    result = requests.post('https://www.reddit.com/api/v1/access_token',
                           auth=auth, data=data, headers=headers)

    token = result.json()['access_token']

    headers['Authorization'] = f'bearer {token}'
    print(headers)

    # Signals a valid connection if response = 200
    print(requests.get('https://oauth.reddit.com/api/v1/me', headers=headers))

    # Result holds top ten posts of listen to this subreddit in a week
    result = requests.get('https://oauth.reddit.com/r/listentothis/top/?t=week', headers=headers,
                          params={'limit': '15'})

    # [data][children] is where posts are kept
    # Iterate through all the posts and gather title and up votes
    # Prints top songs in the console
    for post in result.json()['data']['children']:
        print(post['data']['title']  # Gets post title
              + ' : ' + str(post['data']['ups']) + ' votes'
              + '  ' + post['data']['url'])  # Gets post up votes

    top_songs = []  # A list of top songs
    # Iterate through all top ten posts and get the title
    for post in result.json()['data']['children']:
        song_title = post['data']['title']

        # Splits off unnecessary query information, keeps song title and artist
        song_title = song_title.split('[', 1)[0]
        top_songs.append(song_title)  # Adds the song to the array

    return top_songs


# Searches up all the songs in tracks_array and returns an array of the tracks' IDs
def search_spotify_song(tracks_array, spotify_client_id, spotify_client_secret):
    spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-public",
            client_id=spotify_client_id,
            client_secret=spotify_client_secret,
            redirect_uri='http://localhost:8080/callback'

        ))

    # An array of track ids
    song_id_array = []

    # Search for every song in the tracks array and add their id to the id_array
        for tracks in tracks_array:
        if tracks != '':  # Skips any unsearchable songs
            try:
                song_result = spotify.search(q=tracks, type='track')
                song_id_array.append(
                    song_result['tracks']['items'][0]['id'])  # ID of the top track
            except:
                print('Track: ' + tracks + ' cannot be found')

    return song_id_array


# Adds all the songs from ids_array into the playlist
def add_to_spotify_playlist(ids_array, spotify_client_id, spotify_client_secret):
    spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-public",
            client_id=spotify_client_id,
            client_secret=spotify_client_secret,
            redirect_uri='http://localhost:8080/callback'

        )
    )

    # Adds songs to the playlist
    for song in ids_array:
        # Removes duplicate songs if any
        spotify.playlist_remove_all_occurrences_of_items(playlist_id='6pKOD5vjD948Fcj9QEia9l', items=[song])

        # Song is added
        spotify.playlist_add_items(playlist_id='6pKOD5vjD948Fcj9QEia9l', items=[song])


# Performs all the functions previously (gathers songs and adds songs to playlist)
def automatic_playlist_modification():
    # Code array contains secret codes such as passwords and client IDs
    code_array = read_file_codes()
    red_client_id = code_array[0]
    red_client_secret = code_array[1]
    red_password = code_array[2]
    spot_client_id = code_array[3]
    spot_client_secret = code_array[4]

    # An array of recommended songs from reddit
    recommended_songs = gather_reddit_posts(red_client_id, red_client_secret, red_password)

    # Search the recommended songs on spotify and get their track id's
    track_id_array = search_spotify_song(recommended_songs, spot_client_id, spot_client_secret)

    # Add songs to the playlist
    add_to_spotify_playlist(track_id_array, spot_client_id, spot_client_secret)


# Automates the script to run once a week
schedule.every(7).days.do(automatic_playlist_modification)
# Runs once
automatic_playlist_modification()

# Will run forever once a week
while True:
    schedule.run_pending()
    time.sleep(1)

