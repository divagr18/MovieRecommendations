from django.urls import path
from .views import get_movie_recommendations

app_name = 'MovieName'

urlpatterns = [
    path('get_movie_recommendations/', get_movie_recommendations, name='get_movie_recommendations'),
    # Add other URL patterns as needed
]
