# Auto Start Instructions

## Service File Example

* filename: mything.service
```
[Unit]
Description=mything: do my own thing
After=multi-user.target

[Service]
ExecStart=/usr/local/bin/mything.sh
Restart=always
StartLimitInterval=10
RestartSec=10

[Install]
WantedBy=multi-user.target
```
## Install
* chmod a+rx mything.service
* move to /etc/systemd/system/mything.service
* sudo systemctl enable mything.service