from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms



class CustomUserCreationForm(UserCreationForm):
    
    profile_image = forms.CharField(max_length=150, required=False)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email','profile_image' )



class CustomUserUpdateForm(UserChangeForm):

    gender_choice = [
        ('male', 'male'),
        ('female', 'female')
    ]

    username = forms.CharField(max_length=100, required=True)
    birthday = forms.DateTimeField(required=False)
    gender = forms.CharField(max_length=100, required=True, widget=forms.Select(choices = gender_choice))

    class Meta:
        model = get_user_model()
        fields = ['username', 'profile_image', 'birthday', 'gender']