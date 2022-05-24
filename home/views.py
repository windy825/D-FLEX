from django.shortcuts import render
from django.views.decorators.http import require_safe

from movies.models import Movie
from articles.models import Article
from accounts.models import User


@require_safe
def home(request):
    context = None
    return render(request, 'home/home.html', context)


def search(request):
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


        context = {
            'target' : target,
            'movies' : answer_movies,
            'articles' : answer_article,
            'users' : answer_user,
        }

    return render(request, 'home/search.html', context)