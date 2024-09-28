import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import time

load_dotenv()

def get_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        redirect_uri=os.getenv('REDIRECT_URI'),
        scope="playlist-modify-private",
        open_browser=False,
        cache_path=".spotifycache"
    ))

def extractPlaylistId(url):
    if 'playlist/' in url:
        return url.split('playlist/')[1].split('?')[0]
    return url

def getPlaylistTracks(spotify_user, playlistId, tracks, trackSet):
    offset = 0
    while True:
        results = spotify_user.playlist_items(playlistId, offset=offset)
    
        for idx, item in enumerate(results['items']):
            track = item['track']
            if track is None:
                continue
            artistName = track['artists'][0]['name'] if track['artists'] else 'Unknown Artist'
            trackName = track['name'] if 'name' in track else 'Unknown Track'
            trackId = track['id'] if 'id' in track else None
            
            if trackId and (artistName, trackName) not in trackSet:
                trackSet.add((artistName, trackName))
                tracks.append({
                    'artist': artistName,
                    'track': trackName,
                    'id': trackId
                })
            
        offset += len(results['items'])
        
        if results['next'] is None:
            break

def add_tracks_to_playlist(spotifyUser, playlistId, tracks):
    trackIds = [track['id'] for track in tracks if track['id'] is not None]
    chunkSize = 100
    
    totalAdded = 0
    for i in range(0, len(trackIds), chunkSize):
        chunk = trackIds[i:i + chunkSize]
        
        try:
            spotifyUser.playlist_add_items(playlistId, chunk)
            totalAdded += len(chunk)
            print(f"Added tracks {i+1} to {i+len(chunk)}")
            time.sleep(1)
        
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error adding tracks {i+1} to {i+len(chunk)}: {str(e)}")
            if 'The access token expired' in str(e):
                print("Token expired. Please re-authenticate.")
                return totalAdded
    return totalAdded

# Main execution
spotifyUser = get_spotify_client()

tracks = []
trackSet = set()

playlistUrls  = [
    'https://open.spotify.com/playlist/2S1vcNUX2b7zccyEFfb9ja?si=8ad7e6d56ab0423d',
    'https://open.spotify.com/playlist/4NPTQl7LfvbCVkTuzolFa0?si=a3071f59110f4731',
    'https://open.spotify.com/playlist/7FTFezWPP7vANmapdA4irc?si=100ca5451ce14169',
    'https://open.spotify.com/playlist/1oUs7TIGJ2r3MiOdAIiGvA?si=31103e232d474445',
    'https://open.spotify.com/playlist/7tHiUaTfn9Q87R0mPbAXzk?si=1125cd7d77df495d',
    'https://open.spotify.com/playlist/0ah6E1UBnj1VucMv7WHxTf?si=6a4b49b46f264a65',
    'https://open.spotify.com/playlist/2cqrxmrpesgPwEEBFGaDMi?si=64b6be22727f425e',
    'https://open.spotify.com/playlist/3YwKjViGVuRipe5a950DOu?si=6b3c7595ee9e4578',
    'https://open.spotify.com/playlist/59Mk7lTVmcY1KeDci75ISy?si=8f75d8b44f944331',
    'https://open.spotify.com/playlist/3tUdVJi878cfIsfEznRPzm?si=6b5714d432f743ba'
]

for playlistUrl in playlistUrls:
    playlistId = extractPlaylistId(playlistUrl)
    getPlaylistTracks(spotifyUser, playlistId, tracks, trackSet)

print(f"Total tracks collected: {len(tracks)}")

targetPlaylistId = '7EckjMrKX9mJF6pf9Xevj0'
addedTracks = add_tracks_to_playlist(spotifyUser, targetPlaylistId, tracks)

print(f"Successfully added {addedTracks} tracks to the playlist.")