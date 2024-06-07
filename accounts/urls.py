from django.urls import path, include
from .views import LoginWithPCC
from billboard.views import UserArticleList
urlpatterns = [
    path('', include('allauth.urls')),
    path('confirm/', LoginWithPCC.as_view(), name='confirm'),
    path('user/', UserArticleList.as_view(), name='User'),
]