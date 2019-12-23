# Mopidy setup notes

## mopidy-json-client
[mopidy-json-client](https://github.com/ismailof/mopidy-json-client) though not very active looks like a good library to talk
with mopidy on local from Python. Tried
```sh
pi@rpi:~ $ pip3 install https://github.com/ismailof/mopidy-json-client/archive/master.zip
```
Seemed to work.

# Errors fixed

## Failed to load extension mpd: 'EntryPoint' object has no attribute 'resolve'
```
Traceback (most recent call last):
  File "/usr/lib/python2.7/dist-packages/mopidy/ext.py", line 202, in load_extensions
    extension_class = entry_point.resolve()
```
due to a very old version of setuptools I had installed in local. Solution was to install pip, pip uninstall setuptools 
and then a more recent one that I had was used.
