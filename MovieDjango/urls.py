from django.contrib import admin
from django.urls import path, include
from MovieName.views import get_movie_recommendations

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_movie_recommendations, name='get_movie_recommendations'),
    path('recommendations/', include(('MovieName.urls', 'MovieName'), namespace='MovieName')),
]