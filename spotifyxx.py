import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

#Username from terminal
username = sys.argv[1]
scope = 'user-read-private user-read-playback-state user-modify-playback-state' 

#id 12163157104

#Erase cache prompt for user permission:
try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

#create spotify object with permissions
spotifyObject = spotipy.Spotify(auth=token)

#user information
user = spotifyObject.current_user()
displayName = user['display_name']
follower = user['followers']['total']

while True:

    print()
    print(">>>>Welecome to Spotipy " + displayName + "!")
    print(">>>> You have " + str(follower) + " followers.")
    print()
    print("0 - Search for an artist")
    print("1 - exit")
    print()
    choice = input("Your choice: ")

    #Search for the artist
    if choice == "0":
        print()
        searchQuery = input("OK, what is the artist name: ")
        print()

	#Get search results

        searchResults =  spotifyObject.search(searchQuery,1,0,"artist")
        print(json.dumps(searchResults, sort_keys=True, indent=4))
        
	#artist details
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print(artist['genres'][0])
        print()
        webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']	

        #Album and track details
        trackURIs = []
        trackArt = []
        z = 0
	
	#Extract Album Data
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']
	
        for item in albumResults:
            print("Album " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url'] 

	    #Extract track data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items'] 

            for item in trackResults:
                print(str(z)+ ": " + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z+=1
            print()


        #See Album Art
        while True:
            songSelection = input("Enter a song number to see the album art and play the song(or x to exit): ")
            if songSelection == "x":
    	        break
            webbrowser.open(trackArt[int(songSelection)])



	#End program
    if choice == "1":
        break




#print(json.dumps(VARIABLE, sort_key s=True, indent=4))


