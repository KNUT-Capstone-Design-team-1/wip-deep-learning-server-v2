#!/bin/bash

sudo apt update 

# required lib install
sudo apt install -y python3.8
sudo apt install -y libgl1-mesa-glx libapache2-mod-wsgi
python3 -m pip install --upgrade pip
sudo pip3 install compiler
sudo pip3 install python-dotenv
sudo pip3 install -r /usr/local/wip-deep-learning-server-v2/requirements.txt
sudo python3 /usr/local/wip-deep-learning-server-v2/get_dl_model.py

# service daemon setting
sudo cp ./system/wip-deep-learning-server-v2.service /etc/systemd/system/wip-deep-learning-server-v2.service
sudo systemctl enable wip-deep-learning-server-v2