import json
JSON_DB = 'tracks.json'

with open('./code/tracks.json', 'r') as f:
  tracks_db = json.load(f)['tracks']

def get_track_uris(tag):
  for track in tracks_db:
    if track['tag'] == tag:
      return track['uris']
  else:
      return None
