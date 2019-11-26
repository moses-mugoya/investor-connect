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
    re_path(r'^profile/list/$', views.profiles_list, name='profile_list'),
    re_path(r'^profile/list/investors/$', views.profile_list_investors, name='profile_list_investor'),
    re_path(r'^profile/list/entrepreneur/$', views.profile_list_enterps, name='profile_list_entrep'),
    re_path(r'^profile/list/innovators/$', views.profile_list_innovators, name='profile_list_innovator'),
    re_path(r'^detail/(?P<id>\d+)/', views.profile_detail, name='profile_detail'),
    re_path(r'^edit/note/(?P<id>\d+)/', views.edit_partner_note, name='edit-note'),
    re_path(r'^contact/form/', views.business_management, name='business_management')

]
