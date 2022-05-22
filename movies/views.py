from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_safe, require_http_methods, require_POST

from movies.forms import ReviewForm
from .models import Movie, Review



# path('', views.movies),
@require_safe
def movies(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'movies/movies.html', context)


# path('<int:movie_pk>/', views.movie_detail),
@require_safe
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review_set = movie.review_set.all()
    form = ReviewForm()
    context = {
        'movie': movie,
        'review_set': review_set,
        'review_form': form
    }
    return render(request, 'movies/movie_detail.html', context)


# path('<int:movie_pk>/review/', views.review_create),
@require_POST
def review_create(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
        return redirect('movies:movie_detail', movie.pk)
    return redirect('accounts:login')


# path('<int:movie_pk>/review/<int:review_pk>/update/', views.review_update),
# @login_required
# def review_update(request, movie_pk, review_pk):
#     pass


# path('<int:movie_pk>/review/<int:review_pk>/delete/', views.review_delete),
@require_POST
def review_delete(request, movie_pk, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if request.user == review.user:
            review.delete()
    return redirect('movies:movie_detail', movie_pk)



def for_you(request, movie_pk):
    pick_movie = get_object_or_404(Movie, pk=movie_pk)
    movies = Movie.objects.all()
    movies = [movie for movie in movies if movie.pk != movie_pk]

    # 배우 기반 추천
    actors = pick_movie.actors
    recommend_movies_by_actors = []
    flag = 0
    for movie in movies:
        if flag:
            flag = 0
            continue
        for actor in actors.strip('[]').split(','):
            if flag:
                break
            if actor in movie.actors:
                recommend_movies_by_actors.append(movie)
                flag = 1
                break
    
    
    # 장르 기반 추천
    genres = pick_movie.genres
    recommend_movies_by_genres = []
    for movie in movies:
        if flag:
            flag = 0
            continue
        cnt = 0
        for genre in genres.strip('[]').split(','):
            if genre in movie.genres:
                cnt += 1
                
            if cnt >= 2:
                    recommend_movies_by_genres.append(movie)
                    flag = 1
                    break
    

    # 줄거리 기반 추천
    pick_movie_keywords = pick_movie.overview.replace('.','').replace(',','').split()
    pick_movie_keywords = set([i for i in pick_movie_keywords if i not in {'그', '된다', \
        '되어', '되고', '은', '는', '이', '가', '어느', '있는', '된', '바로', '때', '알게', '통해',\
        '위해', '할', '날', '자신을', '나오는', '무렵', '전부', '수', '자신이', '그가', '마침내',\
        '전', '있음을', '알', '없는', '한', '후', '한', '두' }])
    answer = []
    for movie in movies:
        temp = set(movie.overview.split())
        same_keywords = pick_movie_keywords & temp
        if len(same_keywords) >= 1:
            answer.append([movie.title, same_keywords])
    answer.sort(key= lambda x : len(x[1]), reverse=True)

    context = {
        'recommend_movies_by_actors' : recommend_movies_by_actors,
        'recommend_movies_by_genres' : recommend_movies_by_genres,
        'recommend_movie_by_overview_keywords'  : answer
    }

    return render(request, 'movies/movie_for_you.html', context)
    
    # recommend_movies_by_
