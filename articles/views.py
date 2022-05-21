from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from articles.forms import ArticleForm, CommentForm


from .models import Article

def articles(request):
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        context = {
            'articles':articles,
        }
        return render(request, 'articles:articles', context)

@login_required
def article_create(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = article.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:article_detail', article.pk)
    else:
        form = ArticleForm()
        context = {
            'article_form' : form
        }
        return render(request, 'articles:article_create', context)


@login_required
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    form = CommentForm()
    context = {
        'article':article,
        'comment_form':form
    }
    return render(request, 'articles:article_detail', context)

@login_required
def article_update(request, article_pk):
    pass


@login_required
def article_delete(request, article_pk):
    pass


@login_required
def comment_create(request, article_pk):
    pass


@login_required
def comment_update(request, article_pk, comment_pk):
    pass

@login_required
def comment_delete(request, article_pk, comment_pk):
    pass

