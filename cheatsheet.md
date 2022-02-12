
# Adding support for m4a files
Following error WARNING  Failed local:track:01%20Home%20Recording.m4a: No audio found in file.
```sh
sudo apt-get install gstreamer1.0-plugins-bad
```

# Connecting to the RPI from my MaBook
Well... you definitely need to Authorize Internet Sharing through AX... Gigabit Ethernet adaptor.

Then it's a bit of luck my friend.

Today it worked quickly and I was lucky to find the RPI on 192.168.2.2 by ssh-ing to it.
I had first connected the ethernet cable to everything. The USB ethernet adaptor was showing only a red LED.
Then I turned the RPi's power on. The adaptor started having green and blue light as well.

In my ifconfig I do have a
```
bridge100: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=3<RXCSUM,TXCSUM>
	ether ae:bc:32:9a:7f:64
	inet 192.168.2.1 netmask 0xffffff00 broadcast 192.168.2.255
```

but surprisingly nmap would not have helped:
```sh
nmap -sn 192.168.2.0/24
```
does not list any host on 192.168.2.2 !?

Using
```sh
netstat -rn -finet
```
I do see the RPI on `192.168.2.2`:
```
Destination        Gateway            Flags        Netif Expire
default            192.168.0.1        UGSc           en0
...
192.168.0.255      ff:ff:ff:ff:ff:ff  UHLWbI         en0      !
192.168.2          link#16            UC         bridge1      !
192.168.2.1        ae.bc.32.9a.7f.64  UHLWIi         lo0
192.168.2.2        b8.27.eb.6e.23.f6  UHLWIi     bridge1    858
```

# Putting local files
Tar a folder
```sh
tar -cvf songs_gain.tar ./songs_gain
```

From local
```sh
scp <source> <user>@<dest>/home/<user>/
```

On instance, from home
```sh
sudo mv "01 Home Recording.m4a" /var/lib/mopidy/media/
sudo mopidyctl local scan

# Looks like a restart is needed for the song to be addable in a playlist
sudo systemctl restart mopidy
```

# Mopidy system
Check if service is up
```sh
sudo systemctl status mopidy
```

Check local library content
```sh
sudo cp /var/lib/mopidy/local/library.json.gz .
sudo gunzip library.json.gz
cat library.json
```

# HTTP json rpc
## Check playback status
```sh
curl -d '{"jsonrpc": "2.0", "id": 1, "method": "core.playback.get_state"}' -H 'Content-Type: application/json' http://localhost:6680/mopidy/rpc
```

## Describe methods
```sh
curl -d '{"jsonrpc": "2.0", "id": 1, "method": "core.describe"}' -H 'Content-Type: application/json' http://localhost:6680/mopidy/rpc
```

## Add track into tracklist
```json
{ 
  "core.tracklist.add": {
    "params": [
      { "default": null, "name": "tracks" },
      { "default": null, "name": "at_position" },
      { "default": null, "name": "uri" },
      { "default": null, "name": "uris" }
    ],
    "description": "Add tracks to the tracklist.\n\nIf ``uri`` is given instead of ``tracks``, the URI is looked up in the\nlibrary and the resulting tracks are added to the tracklist.\n\nIf ``uris`` is given instead of ``uri`` or ``tracks``, the URIs are\nlooked up in the library and the resulting tracks are added to the\ntracklist.\n\nIf ``at_position`` is given, the tracks are inserted at the given\nposition in the tracklist. If ``at_position`` is not given, the tracks\nare appended to the end of the tracklist.\n\nTriggers the :meth:`mopidy.core.CoreListener.tracklist_changed` event.\n\n:param tracks: tracks to add\n:type tracks: list of :class:`mopidy.models.Track` or :class:`None`\n:param at_position: position in tracklist to add tracks\n:type at_position: int or :class:`None`\n:param uri: URI for tracks to add\n:type uri: string or :class:`None`\n:param uris: list of URIs for tracks to add\n:type uris: list of string or :class:`None`\n:rtype: list of :class:`mopidy.models.TlTrack`\n\n.. versionadded:: 1.0\n    The ``uris`` argument.\n\n.. deprecated:: 1.0\n    The ``tracks`` and ``uri`` arguments. Use ``uris``."
  }
}
```

```sh
curl -d '{"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.add", "params": {"uris": ["local:track:01%20Home%20Recording.m4a"]}}' \
  -H 'Content-Type: application/json' http://localhost:6680/mopidy/rpc

# Returns :
{"jsonrpc": "2.0", "id": 1, "result": [{"track": {"album": {"__model__": "Album", "name": "Rocky 7"}, "__model__": "Track", "name": "Zonder totetrekkerie", "uri": "local:track:Zonder%20totetrekkerie.mp3", "length": 283864, "last_modified": 1576613541773, "artists": [{"__model__": "Artist", "name": "'t Hof van commerce"}], "genre": "Dance", "bitrate": 127999}, "__model__": "TlTrack", "tlid": 1}]}
```

## Play track
```sh
curl -d '{"jsonrpc": "2.0", "id": 1, "method": "core.playback.play"}' \
  -H 'Content-Type: application/json' http://localhost:6680/mopidy/rpc
```

## Get volume
```sh
curl -d '{"jsonrpc": "2.0", "id": 1, "method": "core.mixer.get_volume"}' \
  -H 'Content-Type: application/json' http://localhost:6680/mopidy/rpc
```

## Get tl_track
```sh
curl -d '{"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.get_tl_tracks"}' \
  -H 'Content-Type: application/json' http://localhost:6680/mopidy/rpc
```
