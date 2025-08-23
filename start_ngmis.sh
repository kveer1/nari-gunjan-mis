#!/bin/bash
echo "Starting Nari Gunjan MIS..."
sudo service postgresql start
cd ~/nari/nari_gunjan_mis
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
