from django.urls import re_path
from . import views


app_name = 'account'


urlpatterns = [
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^verification/docs/uploaded', views.verification_done, name='verification_done'),
    re_path(r'^verification/', views.verify_user, name='verify'),
    re_path(r'^edit/$', views.edit, name='edit'),
    re_path(r'^profile/$', views.profile, name='profile'),
    re_path(r'^personal/(?P<receiver>[-\w]+)/chats/', views.chat_view, name='chat'),
    re_path('^search/', views.user_search, name='search'),
    re_path(r'^profile/list/', views.profiles_list, name='profile_list'),
    re_path(r'^detail/(?P<id>\d+)/', views.profile_detail, name='profile_detail'),
    re_path(r'^contact/form/', views.business_management, name='business_management')

]
