#!/bin/bash
export DISPLAY=:0
gsettings set org.gnome.Vino enabled true
gsettings set org.gnome.Vino prompt-enabled false
gsettings set org.gnome.Vino require-encryption false
gsettings set org.gnome.Vino authentication-methods "['vnc']"
gsettings set org.gnome.Vino vnc-password $(echo -n 'team5607'|base64)
gsettings set org.gnome.settings-daemon.plugins.sharing active true
/usr/lib/vino/vino-server  --display=:0 &
