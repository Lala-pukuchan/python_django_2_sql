import psycopg2
from django.http import HttpResponse

def init(request):
    """
    Create the ex02_movies table if it doesn't exist.
    """
    try:
        conn = psycopg2.connect(
            dbname="djangotraining",
            user="djangouser",
            password="secret",
            host="localhost"
        )
        cur = conn.cursor()
        # テーブル作成SQL
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ex02_movies (
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
    Insert the 7 specified Star Wars movies.
    Each successful insertion -> "OK"
    If an error occurs -> print error message
    """
    movies = [
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
        for movie in movies:
            try:
                cur.execute("""
                    INSERT INTO ex02_movies
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
                # 失敗した場合はそのままエラーをappend
                conn.rollback()
                results.append(f"Error: {e}")
        cur.close()
        conn.close()
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    # 結果を改行で連結して返す
    return HttpResponse("<br>".join(str(r) for r in results))

def display(request):
    """
    Display all data in ex02_movies in an HTML table.
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
        cur.execute("SELECT * FROM ex02_movies;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            return HttpResponse("No data available")

        # HTML table を作成
        html = "<table border='1'>"
        html += "<tr><th>episode_nb</th><th>title</th><th>opening_crawl</th><th>director</th><th>producer</th><th>release_date</th></tr>"
        for row in rows:
            # row = (title, episode_nb, opening_crawl, director, producer, release_date)
            episode_nb = row[1]
            title = row[0]
            opening_crawl = row[2]
            director = row[3]
            producer = row[4]
            release_date = row[5]
            html += f"<tr><td>{episode_nb}</td><td>{title}</td><td>{opening_crawl}</td><td>{director}</td><td>{producer}</td><td>{release_date}</td></tr>"
        html += "</table>"
        return HttpResponse(html)

    except Exception:
        return HttpResponse("No data available")
