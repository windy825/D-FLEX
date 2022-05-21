from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required




# path('', views.movies),
def movies(request):
    pass


# path('<int:movie_pk>/', views.movie_detail),
def movie_detail(request, movie_pk):
    pass


# path('<int:movie_pk>/review/', views.review_create),
def review_create(request, movie_pk):
    pass

# path('<int:movie_pk>/review/<int:review_pk>/update/', views.review_update),
@login_required
def review_update(request, movie_pk, review_pk):
    pass

# path('<int:movie_pk>/review/<int:review_pk>/delete/', views.review_delete),
@login_required
def review_delete(request, movie_pk, review_pk):
    pass