import time
from mopidy_json_client import MopidyClient
from mopidy_json_client.formatting import print_nice

def print_track_info(tl_track):
    track = tl_track.get('track') if tl_track else None
    if not track:
        print('No Track')
        return

    trackinfo = {
        'name': track.get('name'),
        'artists': ', '.join([artist.get('name') for artist in track.get('artists')])
    }
    print('Now playing: {artists} - {name}'.format(**trackinfo))

def show_tracklist(tracklist):
    print_nice('> Current Tracklist: ', tracklist, format='tracklist')

mopidy = MopidyClient()
mopidy.bind_event('track_playback_started', print_track_info)

mopidy.tracklist.get_tl_tracks(on_result=show_tracklist)

mopidy.tracklist.add(uris=['local:track:01%20Home%20Recording.m4a' ,'local:track:Zonder%20totetrekkerie.mp3'])

mopidy.tracklist.get_tl_tracks(on_result=show_tracklist)

mopidy.playback.play()

if __name__ == '__main__':

    # Main loop
    try:
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass