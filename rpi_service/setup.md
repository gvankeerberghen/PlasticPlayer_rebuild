Following https://raspberrypi.stackexchange.com/questions/96673/i-want-to-run-a-python-3-script-on-startup-and-in-an-endless-loop-on-my-raspberr

Create unit:
```sh
sudo systemctl --full --force edit plastic_player_loop.service
```

```
[Unit]
Description=Plastic Player python3 script
After=multi-user.target

[Service]
WorkingDirectory=/home/pi/PlasticPlayer_rebuild
User=pi
ExecStart=/usr/bin/python3 ./code/main_loop.py

[Install]
WantedBy=multi-user.target
```

Enable it to be started on boot up:
```sh
sudo systemctl enable plastic_player_loop.service
```

Check status
```sh
systemctl status plastic_player_loop.service
```
