from django.urls import re_path
from . import views

app_name = 'portal'

urlpatterns = [
    re_path(r'^index/$', views.index, name='index'),
    re_path(r'^$', views.home, name='home'),
    re_path('^search/(?P<id>\d+)/biz', views.biz_user_search, name='search'),
    re_path('^search/(?P<id>\d+)/idea/', views.idea_user_search, name='idea_search'),
    re_path(r'^home/all/business/startups/', views.home_biz, name='home_biz'),
    re_path(r'^centinum/ventures/', views.centinum, name='centinum'),
    re_path(r'investor/business', views.investor, name='investor'),
    re_path(r'investor/idea/', views.investor_idea, name='investor_idea'),
    re_path(r'entrepreneur/', views.entrepreneur, name='entrepreneur'),
    re_path(r'innovator/', views.innovator, name='innovator'),
    re_path(r'investments/business/', views.investments_business, name='investment_biz'),
    re_path(r'investments/', views.investments, name='investments'),
    re_path('^add/idea/', views.add_idea, name='add_idea'),
    re_path('^add/business/startup/', views.add_business, name='add_business'),
    re_path(r'^edit/business/(?P<id>\d+)/', views.edit_business, name='edit_business'),
    re_path(r'^add/idea/', views.add_idea, name='add_idea'),
    re_path(r'^edit/partner', views.edit_partner, name='edit_partner'),
    re_path(r'^edit/idea/(?P<id>\d+)/', views.edit_idea, name='edit_idea'),
    re_path(r'^(?P<id>\d+)/group/', views.group_chat_view, name='group'),
    re_path(r'^(?P<id>\d+)/idea/detail/', views.idea_detail, name='idea_detail'),
    re_path(r'^(?P<id>\d+)/business/detail/', views.business_detail, name='business_detail'),
    re_path(r'^like/business/', views.business_like, name='business_like'),
    re_path(r'^like/idea/', views.idea_like, name='idea_like'),
    re_path(r'^(?P<id>\d+)/accept/idea/request/', views.accept_idea_request, name='accept_idea'),
    re_path(r'^(?P<id>\d+)/decline/idea/request/', views.decline_idea_request, name='decline_idea'),
    re_path(r'^(?P<id>\d+)/accept/business/request/', views.accept_biz_request, name='accept_biz'),
    re_path(r'^(?P<id>\d+)/decline/business/request/', views.decline_biz_request, name='decline_biz'),
    re_path(r'^(?P<id>\d+)/idea/invest/', views.invest_idea, name='idea_invest'),
    re_path(r'^(?P<id>\d+)/business/invest/', views.invest_business, name='invest_business'),
    re_path(r'^(?P<id>\d+)/idea/join/', views.join_idea, name='join_idea'),
    re_path('^add/(?P<id>\d+)/(?P<user_id>\d+)/idea/$', views.add_member_idea, name='add_member_idea'),
    re_path('^add/(?P<id>\d+)/(?P<user_id>\d+)/business/$', views.add_member_biz, name='add_member'),
    re_path('^mark/finished(?P<id>\d+)/$', views.mark_finished_service, name='marked_finished'),
    re_path('^service/timeline(?P<id>\d+)/$', views.service_timeline_chat, name='service_chat'),
    re_path(r'^service/provider/(?P<id>\d+)/', views.service_provider_requests, name='service-provider'),
    re_path(r'^service/detail/(?P<id>\d+)/', views.service_detail, name='service-detail'),
    re_path(r'^(?P<id>\d+)/business/join/', views.join_business, name='join_business'),
    re_path(r'^plan/category/startup/', views.plan_startup_detail, name='plan_startup'),
    re_path(r'^plan/category/pro/', views.plan_pro_detail, name='plan_pro'),
    re_path(r'^plan/category/enterprise/', views.plan_ent_detail, name='plan_ent'),
    re_path(r'terms/conditions/', views.terms, name='terms'),
    re_path(r'privacy/', views.privacy, name='privacy'),
    re_path(r'plans/', views.plans, name='plans'),
    re_path(r'charge/(?P<id>\d+)/', views.charge, name='charge'),
    re_path(r'pay/', views.HomePageView.as_view(), name='pay'),
    re_path(r'^process/$', views.paypal_process, name='process'),
    re_path(r'^done/$', views.payment_done, name='done'),
    re_path(r'^canceled/$', views.payment_canceled, name='canceled'),
    re_path(r'^subscription-failed/$', views.failed_subscription, name='fail'),

]
