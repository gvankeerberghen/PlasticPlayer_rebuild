import json
JSON_DB = 'tracks.json'

all_uris = []

with open('./code/tracks.json', 'r') as f:
  tracks_db = json.load(f)['tracks']

def get_track_uris(tag):
  for track in tracks_db:
    if track['tag'] == tag:
      return track['uris']
  else:
      return None

def get_all_track_uris():
  if not all_uris:
    for track in tracks_db:
      all_uris.extend(track['uris'])
  
  return all_uris
