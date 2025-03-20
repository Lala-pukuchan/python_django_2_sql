from django.shortcuts import render
from .models import Movies, People
from .forms import SearchForm

def search_view(request):
    form = SearchForm(request.POST or None)
    
    # Get unique values of "gender" from People model (excluding empty strings and nulls)
    genders = People.objects.exclude(gender__isnull=True).exclude(gender="").values_list('gender', flat=True).distinct()
    gender_choices = [(g, g) for g in genders]
    form.fields['character_gender'].choices = gender_choices
    
    results = []
    message = ""
    if request.method == "POST" and form.is_valid():
        min_date = form.cleaned_data['min_release_date']
        max_date = form.cleaned_data['max_release_date']
        min_diameter = form.cleaned_data['planet_diameter']
        gender = form.cleaned_data['character_gender']
        
        # First, filter target movies
        movies_qs = Movies.objects.filter(release_date__range=(min_date, max_date))
        # Get people with specified gender, homeworld diameter meeting criteria, and appearing in target movies
        people_qs = People.objects.filter(
            gender=gender,
            homeworld__diameter__gte=min_diameter,
            movies__in=movies_qs
        ).distinct()
        
        # For each character, get movies meeting the criteria
        for person in people_qs:
            valid_movies = person.movies.filter(release_date__range=(min_date, max_date))
            # Only if character has a homeworld
            if person.homeworld:
                for movie in valid_movies:
                    results.append({
                        'film_title': movie.title,          # 1. Film Title
                        'character_name': person.name,      # 2. Character Name
                        'gender': person.gender,            # 3. Gender
                        'homeworld_name': person.homeworld.name,  # 4. Homeworld Name
                        'homeworld_diameter': person.homeworld.diameter,  # 5. Homeworld Diameter
                    })
        
        if not results:
            message = "Nothing corresponding to your research"
    
    context = {
        'form': form,
        'results': results,
        'message': message,
    }
    return render(request, "ex10/search.html", context)
