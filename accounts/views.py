from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from .forms import CustomUserCreationForm
from django.core.paginator import Paginator
from decouple import config
import requests

def oauth(request):
    code = request.GET.get('code', None)
    # print('이것이 code = ' + str(code))
    client_id = request.session.get('client_id')
    redirect_uri = request.session.get('redirect_uri')

    access_token_request_uri = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code&"
    access_token_request_uri += "client_id=" + client_id
    access_token_request_uri += "&redirect_uri=" + redirect_uri
    access_token_request_uri += "&code=" + code

    access_token_request_uri_data = requests.get(access_token_request_uri)
    json_data = access_token_request_uri_data.json()
    access_token = json_data['access_token']
    # print('이것은 access_token = ' + str(access_token))

    url = 'https://kapi.kakao.com/v2/user/me'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/x-www-form-urlencoded; charset-utf-8',
    }
    kakao_response = requests.get(url, headers=headers).json()
    # print('이것이 결과 = ' + str(kakao_response))

    User = get_user_model()

    try:
        email = kakao_response['kakao_account']['email']
    except:
        email = 'kakao_account' + str(kakao_response['id'])

    if User.objects.filter(email = email).exists():
        user = User.objects.get(email = email)
        
        auth_login(request, user)
        return redirect('movies:index')
        
    
    User(
        username = kakao_response['properties']['nickname'],
        last_name = kakao_response['id'],
        email = email,
    ).save()
    user = User.objects.get(email = email)
    
    auth_login(request, user)
    return redirect('movies:index')


def kakao_login(request):
    login_request_uri = 'https://kauth.kakao.com/oauth/authorize?'
    client_id = config('KAKAO_LOGIN_client_id')
    redirect_uri = 'http://13.124.169.106/accounts/oauth'
    login_request_uri += 'client_id=' + client_id
    login_request_uri += '&redirect_uri=' + redirect_uri
    login_request_uri += '&response_type=code'

    request.session['client_id'] = client_id
    request.session['redirect_uri'] = redirect_uri

    return redirect(login_request_uri)








@require_http_methods(['GET', 'POST'])
def signup(request):
    if 'POST' == request.method:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:articles')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    if 'POST' == request.method:
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'home:home')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('home:home')


def user(request):
    pass


def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)
