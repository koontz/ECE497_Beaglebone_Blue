#!/bin/bash
tmux kill-session -t wifi
tmux new-session -s wifi -d './wificonfig.sh'
echo "Wifi started"
echo "look at connection with 'tmux attach -t wifi'"
sleep 0.5
echo "Have to restart network addapter to get an ip Address"
/etc/init.d/networking restart
sleep 1
ifconfig
