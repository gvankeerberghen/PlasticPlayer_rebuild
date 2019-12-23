import json
JSON_DB = 'tracks.json'

with open('filename.txt', 'r') as f:
    tracks_db = json.load(JSON_DB)['tracks']

def getTrackUri(tag):
  for track in tracks_db:
    if track.tag == tag:
      return track.uri
  else:
      return None
