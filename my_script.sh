#!/bin/bash

# step1. source my_script.sh
# step2. pip list
# step3. ./start_server.sh

# Create virtualenv (django_venv)
python3 -m venv django_venv
# Activate virtual environment
source django_venv/bin/activate
# Upgrade pip
pip install --upgrade pip
# Install using requirement.txt
pip install -r requirement.txt
# Virtual environment remains activated after installation
echo "Virtualenv django_venv is activated."
# start server
cd rukobaya
python manage.py runserver
