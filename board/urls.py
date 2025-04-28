from django.urls import path, re_path
from board.views import view_all_ads, home_view, category_view, view_ad_by_id, category_by_id_view, users_view, \
    RegisterAPIView

urlpatterns = [
    path('', home_view, name='home'),
    path('ads/', view_all_ads, name='ads'),
    path('categories/', category_view, name='categories'),
    re_path(r'^category/(?P<category_id>\d+)/$', category_by_id_view, name='category_by_id'),
    re_path(r'^ads/(?P<ad_id>\d+)/$', view_ad_by_id, name='view_ad_by_id'),
    re_path(r'user/(?P<user_id>\d+)/$', users_view, name='user_view'),
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),

]
