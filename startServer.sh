#!/bin/bash
tmux kill-session -t server
tmux new-session -s server -d './webServer/server.py'
echo "Server started"
echo "look at server with 'tmux attach -t server'"

