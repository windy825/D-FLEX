from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from articles.forms import ArticleForm, CommentForm

from .models import Article, Comment



def articles(request):
    if request.method == 'GET':
        articles = Article.objects.order_by('-pk')

        context = {
            'articles':articles,
        }
        return render(request, 'articles/articles', context)


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
        return render(request, 'articles/article_create', context)


@login_required
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    form = CommentForm()
    context = {
        'article':article,
        'comment_form':form
    }
    return render(request, 'articles/article_detail', context)


@login_required
def article_update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                article = form.save(commit=False)
                article.user = request.user
                article.save()
                return redirect('articles:article_detail', article.pk)
        else:
            form = ArticleForm(instance=article)
        context = {
            'article_form': form
        }
        return render(request, 'articles/article_create', context)
    else:
        return redirect('articles:article_detail', article.pk)


@login_required
def article_delete(request, article_pk):
    if request.method == 'POST':
        article = get_object_or_404(Article, pk=article_pk)
        if request.user == article.user:
            article.delete()
    return redirect('articles:articles')


@login_required
def comment_create(request, article_pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    article = get_object_or_404(Article, pk=article_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.article = article
        comment.save()
    return redirect('articles:article_detail', article.pk)


@login_required
def comment_update(request, article_pk, comment_pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    article = get_object_or_404(Article, pk=article_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.article = article
        comment.save()
    return redirect('articles:article_detail', article.pk)


@login_required
def comment_delete(request, article_pk, comment_pk):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('articles:article_detail', article_pk)