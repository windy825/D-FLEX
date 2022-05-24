from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # movie
    path('', views.movies, name='movies'),
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    # review
    path('<int:movie_pk>/reviews/create', views.review_create, name='review_create'),
    path('<int:movie_pk>/reviews/<int:review_pk>/update/', views.review_update, name='review_update'),
    path('<int:movie_pk>/reviews/<int:review_pk>/delete/', views.review_delete, name='review_delete'),
    
    # 영화 추천
    path('for-you/<int:movie_pk>/', views.for_you, name='for_you'),
]