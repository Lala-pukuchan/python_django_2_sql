from django.urls import path
from . import views

urlpatterns = [
    path("", views.search_view, name="ex10_search"),
]
