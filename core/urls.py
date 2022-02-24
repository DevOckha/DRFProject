from django.urls import re_path
from .views import api_root, UserViewSet, ArticleViewSet, CommentViewSet


user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
article_list = ArticleViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
article_detail = ArticleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
comment_detail = CommentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    re_path(
        r'^$', 
        api_root
    ),
    re_path(
        r'^users/$',
        user_list,
        name='user-list'
    ),
    re_path(
        r'^users/(?P<pk>[0-9]+)/$',
        user_detail,
        name='user-detail'
    ),
    re_path(
        r'^articles/$',
        article_list,
        name='article-list'
    ),
    re_path(
        r'^articles/(?P<pk>[0-9]+)/$',
        article_detail,
        name='article-detail'
    ),
    re_path(
        r'^comments/$',
        comment_list,
        name='comment-list'
    ),
    re_path(
        r'^comments/(?P<pk>[0-9]+)/$',
        comment_detail,
        name='comment-detail'
    ),
]