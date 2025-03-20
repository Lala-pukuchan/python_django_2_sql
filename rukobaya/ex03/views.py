from django.http import HttpResponse
from .models import Movies

def populate(request):
    """
    Insert the 7 specified Star Wars movies.
    Each successful insertion -> "OK"
    If an error occurs -> print error message
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
    for movie in data:
        try:
            # The double asterisk (**) operator in Python is used to unpack a dictionary.
            # In this case, the 'movie' dictionary keys are treated as named parameters,
            # and their values are passed to the Movies constructor. For example, 
            # if movie = {"episode_nb": 1, "title": "The Phantom Menace", ...},
            # then Movies(**movie) is equivalent to:
            # Movies(episode_nb=1, title="The Phantom Menace", ...)
            m = Movies(**movie)
            m.save()
            results.append("OK")
        except Exception as e:
            results.append(str(e))
    return HttpResponse("<br>".join(results))

def display(request):
    """
    Display all data in Movies (ex03) as an HTML table.
    If no data or error -> "No data available"
    """
    try:
        movies = Movies.objects.all()
        if not movies:
            return HttpResponse("No data available")
        # Create HTML table
        html = "<table border='1'>"
        html += "<tr><th>episode_nb</th><th>title</th><th>opening_crawl</th><th>director</th><th>producer</th><th>release_date</th></tr>"
        for m in movies:
            html += f"<tr><td>{m.episode_nb}</td><td>{m.title}</td><td>{m.opening_crawl if m.opening_crawl else ''}</td><td>{m.director}</td><td>{m.producer}</td><td>{m.release_date}</td></tr>"
        html += "</table>"
        return HttpResponse(html)
    except Exception:
        return HttpResponse("No data available")
