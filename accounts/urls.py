
#  Accounts app Urls
from accounts import views
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('login/',views.login_page,name='login'),
    path('register/',views.register_page,name='register'),
]
