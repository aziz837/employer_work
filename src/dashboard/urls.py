from django.urls import path

from .views import index, login

app_name = 'dashboard'
urlpatterns = [
    path('', index),
    path('login/', login, name='login'),
]
