from django.urls import path
from myapp.views import *


urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login, name='login'),
    path('users/<int:pk>/', user_detail, name='user_detail'),
    path('user_list/', user_list, name='user_list'),

]