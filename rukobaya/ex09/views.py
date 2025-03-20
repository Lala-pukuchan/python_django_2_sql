from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from .models import Planets, People

def display(request):
    """
    Display all the characters' names, their homeworld as well as the climate,
    which is windy or moderately windy, sorted by character's name in alphabetical order.

    If no data => "No data available, please use the following command line before use:"
    plus the command line for loaddata ex09_initial_data.json
    """
    try:
        # Use select_related("homeworld") to join People and Planets
        qs = People.objects.select_related("homeworld").filter(
            Q(homeworld__climate__icontains='windy') |
            Q(homeworld__climate__icontains='moderately windy')
        ).order_by("name")
        
        people_list = [
            (person.name, person.homeworld.name, person.homeworld.climate)
            for person in qs
            if person.homeworld
        ]

        if not people_list:
            # No data available
            msg = """
            No data available, please use the following command line before use:<br>
            <code>python manage.py loaddata ex09_initial_data.json</code>
            """
            return HttpResponse(msg)

        # build HTML table
        html = "<table border='1'>"
        html += "<tr><th>Name</th><th>Homeworld</th><th>Climate</th></tr>"
        for (pname, planet_name, climate) in people_list:
            html += f"<tr><td>{pname}</td><td>{planet_name}</td><td>{climate}</td></tr>"
        html += "</table>"
        return HttpResponse(html)
    except Exception as e:
        # Same "No data available" + command line
        msg = f"""
        No data available, please use the following command line before use:<br>
        <code>python manage.py loaddata ex09_initial_data.json</code><br>
        Error: {e}
        """
        return HttpResponse(msg)
