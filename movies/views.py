from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_safe, require_http_methods, require_POST

from django.core.paginator import Paginator

from movies.forms import ReviewForm
from .models import Movie, Review

actors_img = []


# path('', views.movies),
@require_safe
def movies(request):
    page = request.GET.get('page', '1')
    movies = Movie.objects.order_by('-release_date')
    MOVIES_PER_PAGE = 40
    paginator = Paginator(movies, MOVIES_PER_PAGE)
    page_movies = paginator.get_page(page)
    context = {
        'movies': page_movies
    }
    return render(request, 'movies/movies.html', context)


# path('<int:movie_pk>/', views.movie_detail),
@require_safe
def movie_detail(request, movie_pk):
    global actors_img
    movie = get_object_or_404(Movie, pk=movie_pk)
    genres = movie.genres.strip('[]').replace("'",'').split(',')[:4]
    movie.overview = movie.overview
    form = ReviewForm()

    # 영상 리스트 by youtube api
    from googleapiclient.discovery import build
    DEVELOPER_KEY = "AIzaSyC1CzkerAIdAl_9mBAjF9m1uPBzOmCvhbs"
    YOUTUBE_API_SERVICE_NAME="youtube"
    YOUTUBE_API_VERSION="v3"
    youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

    search_response_data = youtube.search().list(
    q = movie.title + '영화',
    order = "relevance",
    fields = "items(id)",
    part = "snippet",
    maxResults = 6
    ).execute()['items']

    video_list = []
    for item in search_response_data:
        video = f"https://www.youtube.com/embed/{item['id']['videoId']}?rel=0&controls=0&showinfo=0"
        video_list.append({'video':video})


    import urllib.request
    import json
    client_id = "MB8drhevCnawoQjOxc5S"
    client_secret = "D9wdXNLZar"

    encText = urllib.parse.quote(movie.title+'명장면')
    url = "https://openapi.naver.com/v1/search/image?query=" + encText
    request1 = urllib.request.Request(url)
    request1.add_header("X-Naver-Client-Id",client_id)
    request1.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request1)

    response_body = response.read()
    str_data = response_body.decode('utf-8')
    json_data = json.loads(str_data)
    
    img_movies = []
    for item in json_data['items']:
        if item['thumbnail']:
            img_movies.append({ 'img': item['thumbnail'] })
   

    # 배우정보 크롤링
    img_actors = []
    for actor in movie.actors.strip('[]').split(','):
        actor = actor.strip("''")
        encText = urllib.parse.quote(actor+'얼굴')
        url = "https://openapi.naver.com/v1/search/image?query=" + encText
        request1 = urllib.request.Request(url)
        request1.add_header("X-Naver-Client-Id",client_id)
        request1.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request1)
        
        response_body = response.read()
        answer = response_body.decode('utf-8')
        answer = json.loads(answer)
        if not answer['items']:
            continue
        answer = answer["items"][0]['thumbnail'] if answer['items'] else []
        
        img_actors.append({
            'name':actor,
            'img':answer,
        })
    
    actors_img = img_actors[:]

    context = {
        'movie': movie,
        'review_form': form,
        'genres':genres,
        'video_list':video_list,
        'img_movies':img_movies,
        'img_actors':img_actors,
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
def review_update(request, movie_pk, review_pk):
    pass


# path('<int:movie_pk>/review/<int:review_pk>/delete/', views.review_delete),
@require_POST
def review_delete(request, movie_pk, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if request.user == review.user:
            review.delete()
    return redirect('movies:movie_detail', movie_pk)



def for_you(request, movie_pk):
    global actors_img
    pick_movie = get_object_or_404(Movie, pk=movie_pk)
    movies = Movie.objects.all()
    movies = [movie for movie in movies if movie.pk != movie_pk]
    

    # 배우 기반 추천
    recommend_movies_by_actors = []
    flag = 0
    for movie in movies:
        if flag:
            flag = 0
            continue
        for item in actors_img:
            actor = item['name']
            if flag:
                break
            if actor in movie.actors:
                recommend_movies_by_actors.append({'actor':actor.strip("''"), 'actor_img': [i['img'] for i in actors_img if i['name'] == actor], 'movie':movie})
                flag = 1
                break
    

    
    

    # 줄거리 기반 추천
    pick_movie_keywords = pick_movie.overview.replace('.','').replace(',','').split()
    pick_movie_keywords = set([i for i in pick_movie_keywords if i not in {'그', '된다', \
        '되어', '되고', '은', '는', '이', '가', '어느', '있는', '된', '바로', '때', '알게', '통해',\
        '위해', '할', '날', '자신을', '나오는', '무렵', '전부', '수', '자신이', '그가', '마침내',\
        '전', '있음을', '알', '없는', '한', '후', '한', '두', '될', '채', '더', '그의', '그가', '그는',\
        '모든', '하지만', '최고의' }])
    answer = []
    for movie in movies:
        temp = set(movie.overview.split())
        same_keywords = pick_movie_keywords & temp
        if len(same_keywords) >= 1:
            answer.append([movie.title, same_keywords])
    answer.sort(key= lambda x : len(x[1]), reverse=True)

    context = {
        'recommend_movies_by_actors' : recommend_movies_by_actors,
        'recommend_movie_by_overview_keywords'  : answer[:7],
        'pick_movie' : pick_movie,
    }

    return render(request, 'movies/movie_for_you.html', context)
    
    # recommend_movies_by_

# 장르기반
def for_you2(request, movie_pk):
    pick_movie = get_object_or_404(Movie, pk=movie_pk)
    movies = Movie.objects.all()
    movies = [movie for movie in movies if movie.pk != movie_pk]
    # 장르 기반 추천
    flag = 0
    genres = pick_movie.genres
    recommend_movies_by_genres = []
    for movie in movies:
        if flag:
            flag = 0
            continue
        same_genre = []
        cnt = 0

        for genre in genres.strip('[]').split(','):
            if genre in movie.genres:
                same_genre.append(genre)
                cnt += 1
                
            if cnt >= 3:
                    recommend_movies_by_genres.append({'movie':movie, 'same_genres':same_genre})
                    flag = 1
                    break
    
    context = {
        'recommend_movies_by_genres' : recommend_movies_by_genres,
    }

    return render(request, 'movies/movie_for_you2.html', context)


def for_you3(request, movie_pk):
    pass