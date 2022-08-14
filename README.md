# SpotifyListenToThis
Creating a discovery weekly using r/listentothis

Used python requests package to gather top reddit posts on r/listentothis.
I filter amount the song title and artist from the posts and pipe that to a spotify search by using the Spotipy API.
I then add every song searched into a public playlist to jam out to later.

Notes:
The script is automated every week because I wanted to model it after a discover weekly; however, it's more practical to have the script run once a day in "top posts of the day" rather than the week.
My client IDs and passwords were in a text file for security purposes. Please don't try to hack me 🙏
