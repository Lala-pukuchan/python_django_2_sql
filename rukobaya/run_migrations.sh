#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata ./ex09/ex09_initial_data.json
echo "Migrations completed!"
