from django.shortcuts import render
from django.template import VariableDoesNotExist
from django.views.decorators.http import require_safe

from movies.models import Movie
from articles.models import Article
from accounts.models import User


@require_safe
def home(request):
    context = None
    return render(request, 'home/home.html', context)


def searching(request):
    if request.method == 'POST':
        target = request.POST['search']
        print(target)

        # 영화 제목 일치 여부
        answer_movies = []
        movies = Movie.objects.all()
        for movie in movies:
            if target in movie.title:
                answer_movies.append(movie)
        
        # 게시글 제목 or 내용 일치 여부
        answer_article = []
        articles = Article.objects.all()
        for article in articles:
            if target in article.title or target in article.content:
                answer_article.append(article)

        # 유저 이름 일치 여부
        answer_user = []
        users = User.objects.all()
        for user in users:
            if target in user.username:
                answer_user.append(user)

        # 검색 영상 리스트 by youtube api
        # from googleapiclient.discovery import build
        # DEVELOPER_KEY = "AIzaSyDmvqwqcrhl6vt90DxYBk-BhLhzcBaHJmU"
        # YOUTUBE_API_SERVICE_NAME="youtube"
        # YOUTUBE_API_VERSION="v3"
        # youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

        # search_response_data = youtube.search().list(
        # q = target + ' 영화',
        # order = "relevance",
        # fields = "items(id)",
        # part = "snippet",
        # maxResults = 6
        # ).execute()['items']


        # video_list = []
        # for item in search_response_data:
        #     video = f"https://www.youtube.com/embed/{item['id']['videoId']}?rel=0&controls=0&showinfo=0"
        #     video_list.append({'video': video})

        context = {
            'target' : target,
            'movies' : answer_movies,
            'articles' : answer_article,
            'users' : answer_user,
            'video_list' : [1,2,3,4,5],
        }
    
    return render(request, 'home/search.html', context)