from django.urls import re_path
from . import views


app_name = 'loginApp'


urlpatterns = [
    re_path(r'^login/', views.user_login, name='login'),
]
