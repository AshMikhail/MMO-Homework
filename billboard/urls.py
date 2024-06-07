from django.urls import path
from .views import ArticleDetail, ArticleCreate, ArticleList, ArticleUpdate, ArticleDelete
from .views import CommentCreate, CommentListFilter, CommentDetail, comment_accept, CommentDelete, CommentUpdate, UserCommentList

urlpatterns = [
    path('', ArticleList.as_view(), name='all_articles'),
    path('create', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>', ArticleDetail.as_view(), name='article_detail'),
    path('<int:pk>/update', ArticleUpdate.as_view(), name='article_update'),
    path('<int:pk>/delete', ArticleDelete.as_view(), name='article_delete'),
    path('comment/User/', UserCommentList.as_view(), name='all_user_comments'),
    path('comment/filter', CommentListFilter.as_view(), name='all_comments'),
    path('comment/<int:pk>', CommentDetail.as_view(), name='Comment_Detail'),
    path('comment/<int:pk>/create', CommentCreate.as_view(), name='comment_create'),
    path('comment/<int:pk>/update', CommentUpdate.as_view(), name='comment_Update'),
    path('comment/<int:pk>/accept', comment_accept, name='comment_accept'),
    path('comment/<int:pk>/delete', CommentDelete.as_view(), name='comment_delete'),
]