from django.contrib.auth.views import LogoutView
from django.urls import path
from users.views import UserLogin, CreateUser

app_name = 'users'

urlpatterns = [
    path('login/', UserLogin.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
    path('registration/', CreateUser.as_view(), name='user_create')
]