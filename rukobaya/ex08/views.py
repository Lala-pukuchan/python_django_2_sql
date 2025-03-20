import psycopg2
from django.http import HttpResponse
import os

def init(request):
    """
    Create ex08_planets and ex08_people tables
    with the specified columns and foreign key (homeworld -> ex08_planets.name).
    """
    try:
        conn = psycopg2.connect(
            dbname="djangotraining",
            user="djangouser",
            password="secret",
            host="localhost"
        )
        cur = conn.cursor()

        # 1) Create ex08_planets
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ex08_planets (
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                climate VARCHAR(255),
                diameter INT,
                orbital_period INT,
                population BIGINT,
                rotation_period INT,
                surface_water REAL,
                terrain VARCHAR(128)
            );
        """)

        # 2) Create ex08_people
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ex08_people (
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                birth_year VARCHAR(32),
                gender VARCHAR(32),
                eye_color VARCHAR(32),
                hair_color VARCHAR(32),
                height INT,
                mass REAL,
                homeworld VARCHAR(64),
                CONSTRAINT fk_homeworld
                    FOREIGN KEY(homeworld)
                    REFERENCES ex08_planets(name)
                    ON DELETE SET NULL
            );
        """)

        conn.commit()
        cur.close()
        conn.close()
        return HttpResponse("OK")

    except Exception as e:
        return HttpResponse(f"Error: {e}")

def populate(request):
    """
    Populate ex08_planets and ex08_people from the CSV files.
    Return "OK" for each successful insertion, or error message if failed.
    """
    try:
        conn = psycopg2.connect(
            dbname="djangotraining",
            user="djangouser",
            password="secret",
            host="localhost"
        )
        cur = conn.cursor()

        # 1) Clear existing data to avoid duplication
        cur.execute("TRUNCATE TABLE ex08_people, ex08_planets RESTART IDENTITY CASCADE;")
        conn.commit()

        results = []  # Store results for each operation

        # 2) Copy data from planets.csv → ex08_planets
        base_dir = os.path.dirname(os.path.abspath(__file__))
        planets_path = os.path.join(base_dir, "planets.csv")
        people_path  = os.path.join(base_dir, "people.csv")

        try:
            with open(planets_path, 'r', encoding='utf-8') as f:
                cur.copy_from(
                    f, 
                    'ex08_planets', 
                    sep='\t', 
                    null='NULL',
                    columns=(
                        'name','climate','diameter','orbital_period','population',
                        'rotation_period','surface_water','terrain'
                    )
                )
            conn.commit()
            results.append("OK")
        except Exception as e:
            conn.rollback()
            results.append(f"Error inserting planets: {e}")

        # 3) Copy data from people.csv → ex08_people
        try:
            with open(people_path, 'r', encoding='utf-8') as f:
                cur.copy_from(
                    f,
                    'ex08_people',
                    sep='\t',
                    null='NULL',
                    columns=(
                    'name','birth_year','gender','eye_color','hair_color','height','mass','homeworld'
                    )
                )
            conn.commit()
            results.append("OK")
        except Exception as e:
            conn.rollback()
            results.append(f"Error inserting people: {e}")

        cur.close()
        conn.close()
        return HttpResponse("<br>".join(results))

    except Exception as e:
        return HttpResponse(f"Database connection error: {e}")

def display(request):
    """
    Display all the characters' names, their homeworld as well as the climate
    (which is windy or moderately windy) sorted by character's name in alphabetical order.
    If no data or error, "No data available".
    """
    try:
        conn = psycopg2.connect(
            dbname="djangotraining",
            user="djangouser",
            password="secret",
            host="localhost"
        )
        cur = conn.cursor()
        # characters.name, homeworld, climate
        # only if climate is "windy" or "moderately windy"
        # sorted by character's name
        cur.execute("""
        SELECT p.name AS people_name,
               pl.name AS planet_name,
               pl.climate
        FROM ex08_people p
        JOIN ex08_planets pl ON p.homeworld = pl.name
        WHERE pl.climate LIKE '%windy%' OR pl.climate LIKE '%moderately windy%'
        ORDER BY p.name;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        print(rows)

        if not rows:
            return HttpResponse("No data available")

        # build HTML
        html = "<table border='1'>"
        html += "<tr><th>Name</th><th>Homeworld</th><th>Climate</th></tr>"
        for row in rows:
            people_name = row[0]
            planet_name = row[1]
            climate = row[2]
            html += f"<tr><td>{people_name}</td><td>{planet_name}</td><td>{climate}</td></tr>"
        html += "</table>"
        return HttpResponse(html)

    except Exception as e:
        return HttpResponse("No data available")

