# crushtape
Uses Spotify's web API to generate playlists for your crush.

## Dependencies
The only dependency is [Spotipy](https://github.com/plamere/spotipy). Install it with pip:

`pip3 install spotipy`

## Setup
Since this script requires access to your playlists, you'll have to create a new application at [developer.spotify.com](https://developer.spotify.com/my-applications), and copy the client ID, secret, and redirect URI to *credentials.py*.

## Usage
`python3 crushtape.py --username example "Some Body Once Told Me"`