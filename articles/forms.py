from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    title = forms.CharField()
    content = forms.CharField()

    class Meta:
        model = Article
        fields = ['title', 'content']



class CommentForm(forms.ModelForm):
    content = forms.CharField()

    class Meta:
        model = Comment
        fields = ['content']