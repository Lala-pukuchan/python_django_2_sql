from django.shortcuts import render
from django.http import HttpResponse
from .models import Movies
from .forms import UpdateForm

def populate(request):
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
            # Use get_or_create as there might be an error if episode_nb already exists
            obj, created = Movies.objects.get_or_create(
                episode_nb=movie['episode_nb'],
                defaults=movie
            )
            if created:
                results.append("OK")
            else:
                results.append(f"{movie['title']} already exists.")
        except Exception as e:
            results.append(str(e))
    return HttpResponse("<br>".join(results))

def display(request):
    try:
        movies = Movies.objects.all().order_by('episode_nb')
        if not movies:
            return HttpResponse("No data available")

        html = "<table border='1'>"
        html += "<tr><th>episode_nb</th><th>title</th><th>opening_crawl</th><th>director</th><th>producer</th><th>release_date</th><th>created</th><th>updated</th></tr>"
        for m in movies:
            opening_crawl = m.opening_crawl if m.opening_crawl else ''
            html += f"<tr><td>{m.episode_nb}</td><td>{m.title}</td><td>{opening_crawl}</td><td>{m.director}</td><td>{m.producer}</td><td>{m.release_date}</td><td>{m.created}</td><td>{m.updated}</td></tr>"
        html += "</table>"
        return HttpResponse(html)
    except Exception:
        return HttpResponse("No data available")


def update(request):
    try:
        # Fetch movie list
        movies = Movies.objects.all().order_by('episode_nb')
        if not movies:
            return HttpResponse("No data available")

        # Create (value, label) list for ChoiceField
        choice_list = [(m.title, m.title) for m in movies]

        if request.method == "POST":
            form = UpdateForm(request.POST)
            form.fields['film_title'].choices = choice_list
            if form.is_valid():
                film_to_update = form.cleaned_data['film_title']
                new_crawl = form.cleaned_data['opening_crawl']

                # Get the movie using ORM
                try:
                    movie_obj = Movies.objects.get(title=film_to_update)
                    movie_obj.opening_crawl = new_crawl
                    movie_obj.save()  # This will automatically update the 'updated' field to current timestamp
                except Movies.DoesNotExist:
                    pass
        else:
            form = UpdateForm()
            # Set choices for GET request as well
            form.fields['film_title'].choices = choice_list

        # Fetch again and check if empty
        movies = Movies.objects.all().order_by('episode_nb')
        if not movies:
            return HttpResponse("No data available")

        # Create form again (same for after POST)
        choice_list = [(m.title, m.title) for m in movies]
        form = UpdateForm()
        form.fields['film_title'].choices = choice_list

        return render(request, "ex07/update.html", {"form": form})

    except Exception as e:
        return HttpResponse(f"No data available {e}")
