from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.core.paginator import Paginator
from decouple import config
import requests

def oauth(request):
    code = request.GET.get('code', None)
    client_id = request.session.get('client_id')
    redirect_uri = request.session.get('redirect_uri')

    access_token_request_uri = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code&"
    access_token_request_uri += "client_id=" + client_id
    access_token_request_uri += "&redirect_uri=" + redirect_uri
    access_token_request_uri += "&code=" + code

    access_token_request_uri_data = requests.get(access_token_request_uri)
    json_data = access_token_request_uri_data.json()
    access_token = json_data['access_token']

    url = 'https://kapi.kakao.com/v2/user/me'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/x-www-form-urlencoded; charset-utf-8',
    }
    kakao_response = requests.get(url, headers=headers).json()

    User = get_user_model()

    try:
        email = kakao_response['kakao_account']['email']
    except:
        email = 'kakao_account' + str(kakao_response['id'])

    if User.objects.filter(email = email).exists():
        user = User.objects.get(email = email)
        
        auth_login(request, user)
        return redirect('home:home')
        
    
    User(
        username = kakao_response['properties']['nickname'],
        last_name = kakao_response['id'],
        profile_image = kakao_response['properties']['profile_image'],
        thumbnail_image = kakao_response['properties']['thumbnail_image'],
        birthday = kakao_response['kakao_account']['birthday'],
        gender = kakao_response['kakao_account']['gender'],
        email = email,
    ).save()

    user = User.objects.get(email = email)
    
    auth_login(request, user)
    return redirect('home:home')


def kakao_login(request):
    login_request_uri = 'https://kauth.kakao.com/oauth/authorize?'
    client_id = config('KAKAO_LOGIN_client_id')
    redirect_uri = 'http://127.0.0.1:8000/accounts/auth'
    login_request_uri += 'client_id=' + client_id
    login_request_uri += '&redirect_uri=' + redirect_uri
    login_request_uri += '&response_type=code'

    request.session['client_id'] = client_id
    request.session['redirect_uri'] = redirect_uri

    return redirect(login_request_uri)

def kakao_unlink(request):
    unlink_request_url = 'https://kapi.kakao.com/v1/user/unlink'
    User = get_user_model()
    user = User.objects.get(email = request.user.email)
    headers = {
        'Authorization': config('ADMIN_KEY'),
    }
    params = {
        'Authorization': config('ADMIN_KEY'),
        'target_id': user.last_name,
        'target_id_type': "user_id",
    }
    unpluged = requests.post(unlink_request_url, headers=headers, params=params).json()
    auth_logout(request)
    user.delete()
    return redirect('home:home')


@require_http_methods(['GET', 'POST'])
def signup(request):
    if 'POST' == request.method:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            'https://user-images.githubusercontent.com/89068148/170427885-7cfa46be-c5a8-48c8-bc7e-cb8ffe19ca93.png'
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
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form':form,
    }
    return render(request, 'accounts/change_password.html', context)


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


@login_required
def update(request):
    if request.method == 'POST':
        change_from = CustomUserUpdateForm(request.POST, instance=request.user)
        if change_from.is_valid():
            change_from.save()
            return redirect('accounts:profile', request.user.username)
    else:
	    change_from = CustomUserUpdateForm(instance=request.user)
    context = {
        'form':change_from
    }
    return render(request, 'accounts/update.html', context)


def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)
