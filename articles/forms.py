from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):

    title = forms.CharField(
        label='제목',
    )

    content = forms.CharField(
        label='내용',
    )

    class Meta:
        model = Article
        fields = ['title', 'content']



class CommentForm(forms.ModelForm):
    
    CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]
    rating = forms.IntegerField(
        label='별점',
        widget=forms.Select(
            choices = CHOICES,
            attrs={
                'style': 'width: 10rem;'
            }
        )
    )

    
    content = forms.CharField(
        label='리뷰 내용',
        help_text='200자 이내',
        widget=forms.Textarea(
            attrs={'style': 'height: 10rem;'}
        ),
    )


    class Meta:
        model = Comment
        fields = ['content', 'rating']