#!/bin/bash
apt-get update
apt-get install -y libgl1
/usr/local/bin/python -m pip install --upgrade pip
pip install --upgrade setuptools
pip install --upgrade wheel
pip install -r /app/requirements.txt
cd /app
clear
/usr/local/bin/python -u app.py