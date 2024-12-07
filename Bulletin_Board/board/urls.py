from django.urls import path
from .views import AdsList, AdsCreate, AdsUpdate, ReplyAdd, Replies, delete_reply, delete_ads, \
 allow_reply, news_send
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.AdsList.as_view(), name='ads_list'),
    path('create/', AdsCreate.as_view(), name='create'),
    path('<int:pk>/edit/', AdsUpdate.as_view(), name='ads_edit'),
    path('<int:pk>/reply/add', ReplyAdd.as_view(), name='reply_add'),
    path('replies/', Replies.as_view(), name='replies'),
    path('delete/<int:pk>', delete_reply, name='delete_reply'),
    path('<int:pk>/delete', delete_ads, name='delete_post'),
    path('<int:pk>/allow', allow_reply, name='allow_reply'),
    path('send_mails/', news_send, name='send_mails'),

]
