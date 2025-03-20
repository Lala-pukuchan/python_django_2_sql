#!/bin/bash

python manage.py makemigrations
python manage.py migrate

echo "Migrations completed!"

python manage.py loaddata ./ex09/ex09_initial_data.json
python manage.py loaddata ./ex10/ex10_initial_data.json

echo "Initial data loaded!"
