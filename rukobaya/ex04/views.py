import psycopg2
from django.http import HttpResponse
from django.shortcuts import render
from .forms import RemoveForm

def init(request):
    """
    Create the ex04_movies table if it doesn't exist.
    Same structure as ex00, but table name is ex04_movies.
    """
    try:
        conn = psycopg2.connect(
            dbname="djangotraining",
            user="djangouser",
            password="secret",
            host="localhost"
        )
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ex04_movies (
                title VARCHAR(64) UNIQUE NOT NULL,
                episode_nb INTEGER PRIMARY KEY,
                opening_crawl TEXT,
                director VARCHAR(32) NOT NULL,
                producer VARCHAR(128) NOT NULL,
                release_date DATE NOT NULL
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
    Insert the 7 Star Wars movies. If already removed, they should be re-inserted (no conflict).
    Return "OK" or error message.
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
                cur.execute("""
                    INSERT INTO ex04_movies
                    (episode_nb, title, director, producer, release_date)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (episode_nb)
                    DO NOTHING;
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
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    return HttpResponse("<br>".join(results))

def display(request):
    """
    Display all the data in ex04_movies.
    If no data or error, display "No data available".
    """
    try:
        conn = psycopg2.connect(
            dbname="djangotraining",
            user="djangouser",
            password="secret",
            host="localhost"
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM ex04_movies;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            return HttpResponse("No data available")

        # row = (title, episode_nb, opening_crawl, director, producer, release_date)
        html = "<table border='1'>"
        html += "<tr><th>episode_nb</th><th>title</th><th>opening_crawl</th><th>director</th><th>producer</th><th>release_date</th></tr>"
        for row in rows:
            title = row[0]
            episode_nb = row[1]
            opening_crawl = row[2] if row[2] else ''
            director = row[3]
            producer = row[4]
            release_date = row[5]
            html += f"<tr><td>{episode_nb}</td><td>{title}</td><td>{opening_crawl}</td><td>{director}</td><td>{producer}</td><td>{release_date}</td></tr>"
        html += "</table>"
        return HttpResponse(html)
    except Exception:
        return HttpResponse("No data available")

#def remove(request):
#    try:
#        conn = psycopg2.connect(
#            dbname="djangotraining",
#            user="djangouser",
#            password="secret",
#            host="localhost"
#        )
#        cur = conn.cursor()

#        print(f"Request method: {request.method}")
#        cur.execute("SELECT title FROM ex04_movies ORDER BY episode_nb;")
#        rows = cur.fetchall()
#        cur.close()
#        conn.close()

#        print('rows:', rows)
        
#        if not rows:
#            return HttpResponse("No data available！！！")

#        choice_list = [(row[0], row[0]) for row in rows]

#        # POST processing
#        if request.method == "POST":
#            form = RemoveForm(request.POST)
#            form.fields['film_title'].choices = choice_list


#            if form.is_valid():
#                film_to_remove = form.cleaned_data['film_title']

#                print(f"Removing {film_to_remove}")

#                # Delete using SQL
#                cur.execute("DELETE FROM ex04_movies WHERE title = %s;", [film_to_remove])
#                conn.commit()

#            else:
#                print("Form is not valid:", form.errors)

#        # Fetch movie list again and set it to form's ChoiceField
#        cur.execute("SELECT title FROM ex04_movies ORDER BY episode_nb;")
#        rows = cur.fetchall()
#        cur.close()
#        conn.close()

#        if not rows:
#            return HttpResponse("No data available")

#        # Set title list to field's choices
#        choice_list = [(row[0], row[0]) for row in rows]  # (value, label)
#        form = RemoveForm()
#        form.fields['film_title'].choices = choice_list

#        return render(request, "ex04/remove.html", {"form": form})

#    except Exception as e:
#        return HttpResponse(f"No data available but why? {e}")

def remove(request):
    try:
        conn = psycopg2.connect(
            dbname="djangotraining",
            user="djangouser",
            password="secret",
            host="localhost"
        )
        cur = conn.cursor()

        print(f"Request method: {request.method}")

        cur.execute("SELECT title FROM ex04_movies ORDER BY episode_nb;")
        rows = cur.fetchall()

        if not rows:
            cur.close()
            conn.close()
            return HttpResponse("No data available")

        choice_list = [(row[0], row[0]) for row in rows]

        if request.method == "POST":
            form = RemoveForm(request.POST)
            form.fields['film_title'].choices = choice_list

            if form.is_valid():
                film_to_remove = form.cleaned_data['film_title']
                print(f"Removing {film_to_remove}")
                cur.execute("DELETE FROM ex04_movies WHERE title = %s;", [film_to_remove])
                conn.commit()
            else:
                print("Form is not valid:", form.errors)

        cur.execute("SELECT title FROM ex04_movies ORDER BY episode_nb;")
        rows = cur.fetchall()
        if not rows:
            cur.close()
            conn.close()
            return HttpResponse("No data available")

        choice_list = [(row[0], row[0]) for row in rows]
        form = RemoveForm()
        form.fields['film_title'].choices = choice_list

        cur.close()
        conn.close()
        return render(request, "ex04/remove.html", {"form": form})

    except Exception as e:
        return HttpResponse(f"No data available but why? {e}")
