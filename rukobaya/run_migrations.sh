#!/bin/bash

python manage.py makemigrations
python manage.py migrate

echo "Migrations completed!"
