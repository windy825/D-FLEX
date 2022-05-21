from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):

    CHOICES= [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★')
    ]
    rating = forms.IntegerField(
        label='별점',
        widget=forms.Select(
            choices = CHOICES,
        )
    )

    content = forms.CharField(
        label='리뷰',
        widget=forms.Textarea()
        
    )

    class Meta:
        model = Review
        fields = ['content', 'rating']