# ex00/urls.py
from django.urls import path
from .views import init  # ex00/views.py に定義された init ビューをインポート

urlpatterns = [
    path('init/', init, name='ex00_init'),
]
