import requests
import logging

logger = logging.getLogger('mopidy_client')

RPC_URL = 'http://localhost:6680/mopidy/rpc'
TIMEOUT = 3

def play_new_tracks(track_uris, random = False):
  try:
    requests.post(RPC_URL, json={"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.clear"}, timeout=TIMEOUT)
    requests.post(RPC_URL, json={"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.add", "params": {"uris": track_uris}}, timeout=TIMEOUT)
    requests.post(RPC_URL, json={"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.set_random", "params": {"value": random}}, timeout=TIMEOUT)
    requests.post(RPC_URL, json={"jsonrpc": "2.0", "id": 1, "method": "core.playback.play"}, timeout=TIMEOUT)
  except requests.Timeout:
    logger.debug('Play new track request timeout')

def stop_track():
  try:
    requests.post(RPC_URL, json={"jsonrpc": "2.0", "id": 1, "method": "core.playback.stop"}, timeout=TIMEOUT)
  except requests.Timeout:
    logger.debug('Play new track request timeout')
