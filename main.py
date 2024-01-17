import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import webbrowser


#songs
data_frame = pd.read_csv('SpotifyFeatures.csv')

username = ''
clientID = ''
clientSecret = ''
redirect_uri = 'http://google.com/callback/'
scope = "user-modify-playback-state user-read-currently-playing user-read-playback-state"

oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri, scope=scope) 
token_dict = oauth_object.get_access_token() 
token = token_dict['access_token'] 
spotifyObject = spotipy.Spotify(auth=token) 
user_name = spotifyObject.current_user() 

  
# To print the response in readable format. 
print(json.dumps(user_name, sort_keys=True, indent=4)) 


while True: 
    print("Welcome to the project, " + user_name['display_name']) 
    print("0 - Exit the console") 
    print("1 - Search for a Song")
    print("2 - play a Song")
    print("3 - play random song from dataset")
    print("4 - Next track")
    print("5 - Add 5 random songs to queue")
    user_input = int(input("Enter Your Choice: ")) 
    if user_input == 1:
        search_song = input("Enter the song name: ") 
        results = spotifyObject.search(search_song, 1, 0, "track") 
        songs_dict = results['tracks']
        song_items = songs_dict['items']
        song = song_items[0]['external_urls']['spotify']
        webbrowser.open(song) 
        print('Song has opened in your browser.')
    elif user_input == 2:
        track_id = input("Enter the track id: ")
        spotifyObject.start_playback(uris=[f'spotify:track:{track_id}'])
    elif user_input == 3:
        track_id = data_frame.sample(n=1)
        track_id = track_id['track_id']
        track_id = track_id.values[0]
        print(track_id)
        spotifyObject.start_playback(uris=[f'spotify:track:{track_id}'])
    elif user_input == 4:
        spotifyObject.next_track()
    elif user_input == 5:
        # add 5 random songs from dataset to queue
        track_id = data_frame.sample(n=5)
        track_id = track_id['track_id']
        track_id = track_id.values
        for i in range(5):
            #print(track_id[i])
            spotifyObject.add_to_queue(f'spotify:track:{track_id[i]}')
        spotifyObject.next_track()
        spotifyObject.queue()
    elif user_input == 0: 
        print("Good Bye, Have a great day!") 
        break

    else: 
        print("Please enter valid user-input.") 
