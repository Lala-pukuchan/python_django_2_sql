import psycopg2
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UpdateForm

def init(request):
    """
    Create ex06_movies table with created & updated fields,
    plus the trigger for auto-updating 'updated' on row change.
    """
    try:
        conn = psycopg2.connect(
            dbname="djangotraining",
            user="djangouser",
            password="secret",
            host="localhost"
        )
        cur = conn.cursor()

        # 1) Create table
        # Choose appropriate type for created/updated (TIMESTAMP or TIMESTAMP WITH TIME ZONE)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ex06_movies (
                title VARCHAR(64) UNIQUE NOT NULL,
                episode_nb INTEGER PRIMARY KEY,
                opening_crawl TEXT,
                director VARCHAR(32) NOT NULL,
                producer VARCHAR(128) NOT NULL,
                release_date DATE NOT NULL,
                created TIMESTAMP DEFAULT NOW(),
                updated TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()

        # 2) Define function for trigger
        cur.execute("""
            CREATE OR REPLACE FUNCTION update_changetimestamp_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated = now();
                NEW.created = OLD.created;
                RETURN NEW;
            END;
            $$ language 'plpgsql';
        """)
        conn.commit()

        # 3) Create trigger
        cur.execute("""
            CREATE TRIGGER update_films_changetimestamp
            BEFORE UPDATE ON ex06_movies
            FOR EACH ROW
            EXECUTE PROCEDURE update_changetimestamp_column();
        """)
        conn.commit()

        cur.close()
        conn.close()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def populate(request):
    """
    Insert 7 Star Wars movies (same as ex02).
    Return 'OK' or error message for each insertion.
    """
    data = [
        {
            'episode_nb': 1,
            'title': 'The Phantom Menace',
            'director': 'George Lucas',
            'producer': 'Rick McCallum',
            'release_date': '1999-05-19'
        },
        {
            'episode_nb': 2,
            'title': 'Attack of the Clones',
            'director': 'George Lucas',
            'producer': 'Rick McCallum',
            'release_date': '2002-05-16'
        },
        {
            'episode_nb': 3,
            'title': 'Revenge of the Sith',
            'director': 'George Lucas',
            'producer': 'Rick McCallum',
            'release_date': '2005-05-19'
        },
        {
            'episode_nb': 4,
            'title': 'A New Hope',
            'director': 'George Lucas',
            'producer': 'Gary Kurtz, Rick McCallum',
            'release_date': '1977-05-25'
        },
        {
            'episode_nb': 5,
            'title': 'The Empire Strikes Back',
            'director': 'Irvin Kershner',
            'producer': 'Gary Kurtz, Rick McCallum',
            'release_date': '1980-05-17'
        },
        {
            'episode_nb': 6,
            'title': 'Return of the Jedi',
            'director': 'Richard Marquand',
            'producer': 'Howard G. Kazanjian, George Lucas, Rick McCallum',
            'release_date': '1983-05-25'
        },
        {
            'episode_nb': 7,
            'title': 'The Force Awakens',
            'director': 'J. J. Abrams',
            'producer': 'Kathleen Kennedy, J. J. Abrams, Bryan Burk',
            'release_date': '2015-12-11'
        },
    ]
    results = []
    try:
        conn = psycopg2.connect(
            dbname="djangotraining",
            user="djangouser",
            password="secret",
            host="localhost"
        )
        cur = conn.cursor()
        for movie in data:
            try:
                # insertion
                cur.execute("""
                    INSERT INTO ex06_movies
                    (episode_nb, title, director, producer, release_date)
                    VALUES (%s, %s, %s, %s, %s);
                """, (
                    movie['episode_nb'],
                    movie['title'],
                    movie['director'],
                    movie['producer'],
                    movie['release_date']
                ))
                conn.commit()
                results.append("OK")
            except Exception as e:
                conn.rollback()
                results.append(f"Error: {e}")
        cur.close()
        conn.close()
        return HttpResponse("<br>".join(results))
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def display(request):
    """
    Display all ex06_movies in an HTML table.
    If no data or error -> "No data available"
    """
    try:
        conn = psycopg2.connect(
            dbname="djangotraining",
            user="djangouser",
            password="secret",
            host="localhost"
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM ex06_movies;")
        rows = cur.fetchall()  # row = (title, episode_nb, opening_crawl, director, producer, release_date, created, updated)
        cur.close()
        conn.close()

        if not rows:
            return HttpResponse("No data available")

        html = "<table border='1'>"
        html += "<tr><th>episode_nb</th><th>title</th><th>opening_crawl</th><th>director</th><th>producer</th><th>release_date</th><th>created</th><th>updated</th></tr>"
        for row in rows:
            title = row[0]
            episode_nb = row[1]
            opening_crawl = row[2] if row[2] else ''
            director = row[3]
            producer = row[4]
            release_date = row[5]
            created = row[6]
            updated = row[7]
            html += f"<tr><td>{episode_nb}</td><td>{title}</td><td>{opening_crawl}</td><td>{director}</td><td>{producer}</td><td>{release_date}</td><td>{created}</td><td>{updated}</td></tr>"
        html += "</table>"
        return HttpResponse(html)
    except Exception:
        return HttpResponse("No data available")


def update(request):
    """
    Displays a form with a drop-down list of existing films + a text field for new crawl.
    When validated, updates the chosen film's opening_crawl in ex06_movies.
    If no data or error -> "No data available"
    """
    try:
        conn = psycopg2.connect(
            dbname="djangotraining",
            user="djangouser",
            password="secret",
            host="localhost"
        )
        cur = conn.cursor()

        # 1) Fetch movie list
        cur.execute("SELECT title FROM ex06_movies ORDER BY episode_nb;")
        rows = cur.fetchall()
        
        # If rows is empty, no data available
        if not rows:
            cur.close()
            conn.close()
            return HttpResponse("No data available")

        # Create (value, label) list for ChoiceField
        choice_list = [(row[0], row[0]) for row in rows]

        # 2) If POST, bind the form
        if request.method == "POST":
            form = UpdateForm(request.POST)
            # Reset choices after form creation
            form.fields['film_title'].choices = choice_list

            if form.is_valid():
                # If validation OK, proceed with update
                film_to_update = form.cleaned_data['film_title']
                new_crawl = form.cleaned_data['opening_crawl'] or ""
                try:
                    cur.execute("""
                        UPDATE ex06_movies
                        SET opening_crawl = %s
                        WHERE title = %s;
                    """, [new_crawl, film_to_update])
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    return HttpResponse(f"Error while updating: {e}")
        else:
            # For GET request, create empty form
            form = UpdateForm()
            form.fields['film_title'].choices = choice_list

        # 3) Finally close cursor/connection
        cur.close()
        conn.close()

        # 4) Pass form to template for rendering
        return render(request, "ex06/update.html", {"form": form})

    except Exception as e:
        return HttpResponse(f"No data available {e}")
