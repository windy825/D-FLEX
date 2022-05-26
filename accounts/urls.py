from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<username>', views.profile, name='profile'),
    path('update/', views.update, name='update'),
    path('password/', views.change_password, name='change_password'),

    #kakao 
    path('kakao_login/', views.kakao_login, name='kakao_login'),
    path('kakao_unlink/', views.kakao_unlink, name='kakao_unlink'),
    path('auth/', views.oauth, name='auth'),
]
