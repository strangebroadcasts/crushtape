"""
crushtape.py

Generate a Spotify playlist with song titles forming a message.
"""
import argparse
import difflib
import itertools
import shlex

import spotipy
import spotipy.util

import credentials

def find_song(spotify, query, matchRatio=0.75):
    """Search Spotify for a song with a title close to the query."""
    results = spotify.search("track:\"" + query + "\"", limit=50, type='track')
    candidates = list(map(lambda track: {'name': track['name'], 'uri': track['uri']}, 
        results['tracks']['items']))
    for candidate in candidates:
        matcher = difflib.SequenceMatcher(None, candidate['name'].lower(), query.lower())
        if matcher.ratio() >= matchRatio:
            print("Adding song " + candidate["name"] + " for " + query)
            return candidate['uri']
    print("Found no matches for " + query)
    return None

def approximate_message(spotify, message_tokens, args):
    """Attempt to generate a list of songs with titles forming the given message."""
    uris = []
    while len(message_tokens) > 0:
        foundTrack = False
        # First, try searching for a single word.
        for tokens in range(1, args.searchterms + 1):
            currentQuery = ' '.join(itertools.islice(message_tokens, tokens))
            print("Trying to search for " + currentQuery)
            closestSong = find_song(spotify, currentQuery, args.ratio)
            if closestSong != None:
                foundTrack = True
                uris.append(closestSong)
                message_tokens = message_tokens[tokens:]
                break
        if not foundTrack:
            print("Couldn't find any tracks matching " + message_tokens[0] + ", skipping")
            message_tokens.pop(0)

    return uris


def compose_playlist(spotify, message, args):
    message_tokens = shlex.split(message)
    song_uris = approximate_message(spotify, message_tokens, args)
    playlist = spotify.user_playlist_create(args.username, args.title, public=False)
    spotify.user_playlist_add_tracks(args.username, playlist['id'], song_uris)

def main():
    parser = argparse.ArgumentParser(prog="crushtape")
    parser.add_argument("--username", required=True)
    parser.add_argument("--title", default="Playlist For My Crush")
    parser.add_argument("--ratio", type=float, default=0.95)
    parser.add_argument("--searchterms", type=int, default=3)
    parser.add_argument("message")
    args = parser.parse_args()
    
    scope = "playlist-modify-private"
    authToken = spotipy.util.prompt_for_user_token(args.username, 
        scope, 
        client_id=credentials.SPOTIPY_CLIENT_ID, 
        client_secret=credentials.SPOTIPY_CLIENT_SECRET, 
        redirect_uri=credentials.SPOTIPY_REDIRECT_URI)
    if authToken:
        sp = spotipy.Spotify(auth=authToken)
        compose_playlist(sp, args.message, args)
    else:
        print("Couldn't get authentication token for " + args.username)
        return

if __name__ == '__main__':
    main()