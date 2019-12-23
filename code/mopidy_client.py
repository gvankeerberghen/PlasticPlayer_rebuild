import requests
import logging

logger = logging.getLogger('mopidy_client')

RPC_URL = 'http://localhost:6680/mopidy/rpc'
TIMEOUT = 3

def play_new_track(track_uri):
  msg_id = 0
  try:
    requests.post(RPC_URL, json={"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.clear"}, timeout=TIMEOUT)
    msg_id += 1
    requests.post(RPC_URL, json={"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.add", "params": {"uris": [track_uri]}}, timeout=TIMEOUT)
    msg_id += 1
    requests.post(RPC_URL, json={"jsonrpc": "2.0", "id": 1, "method": "core.playback.play"}, timeout=TIMEOUT)
    msg_id += 1
  except requests.Timeout:
    logger.debug('Play new track request timeout')

def stop_track():
  try:
    requests.post(RPC_URL, json={"jsonrpc": "2.0", "id": 1, "method": "core.playback.stop"}, timeout=TIMEOUT)
  except requests.Timeout:
    logger.debug('Play new track request timeout')
