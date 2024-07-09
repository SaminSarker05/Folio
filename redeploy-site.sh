#!/bin/bash

tmux kill-server

cd /root/Folio

git fetch && git reset origin/main --hard

source folio-venv/bin/activate

pip install -r requirements.txt

tmux new-session -d -s flask 'flask run --host=0.0.0.0'
