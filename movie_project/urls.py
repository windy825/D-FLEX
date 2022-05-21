from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('articles/', include('articles.urls')),
    path('movies/', include('movies.urls')),

]