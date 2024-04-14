# I created a service for the python loop to start on reboot
In `/etc/systemd/system/plastic_player_loop.service`

```
[Unit]
Description=Plastic Player python3 script
After=multi-user.target

[Service]
WorkingDirectory=/home/pi/PlasticPlayer_rebuild
User=pi
ExecStart=/usr/bin/python3 ./code/main_loop.py
Restart=on-failure
RestartSec=1

[Install]
WantedBy=multi-user.target
```
