# Spotify Playlist Aggregator

A Python script that combines tracks from multiple Spotify playlists into a single target playlist, removing duplicates in the process.

## Features

- Authenticates with Spotify using OAuth
- Extracts tracks from multiple source playlists
- Removes duplicate tracks based on artist and track name
- Adds unique tracks to a target playlist
- Handles pagination for large playlists
- Rate limiting protection with sleep intervals
- Token expiration handling
- Progress tracking during track addition

## Prerequisites

- Python 3.x
- Spotify Developer Account
- Required Python packages:
  - `spotipy`
  - `python-dotenv`

## Setup

1. Create a Spotify Developer Application at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

2. Create a `.env` file in the project root with your Spotify credentials:

```env
CLIENT_ID=your_client_id_here
CLIENT_SECRET=your_client_secret_here
REDIRECT_URI=your_redirect_uri_here
```

3.Install Required Packages

```bash
pip install spotipy python-dotenv
```

## Usage

1. Add your source playlist URLs to the `playlistUrls` list in main.py

2. Set your target playlist ID in the `targetPlaylistId` variable

3. Run the script:

```sh
python main.py
```

## How It Works

1. The script authenticates with Spotify using the credentials in your `.env` file
2. It processes each source playlist URL to extract track information
3. Tracks are stored in a list while maintaining a set to prevent duplicates
4. Finally, tracks are added to the target playlist in chunks of 100 (Spotify API limit)

## Functions

- `get_spotify_client()`: Initializes the Spotify client with OAuth authentication
- `extractPlaylistId(url)`: Extracts the playlist ID from a Spotify playlist URL
- `getPlaylistTracks(spotify_user, playlistId, tracks, trackSet)`: Retrieves all tracks from a playlist
- `add_tracks_to_playlist(spotifyUser, playlistId, tracks)`: Adds tracks to the target playlist

## Error Handling

- Handles missing track information gracefully
- Manages API rate limits
- Handles token expiration
- Provides feedback on progress and errors

## Notes

- The script requires playlist-modify-private scope
- A `.spotifycache` file will be created to store authentication tokens
- The script includes a 1-second delay between track additions to prevent rate limiting