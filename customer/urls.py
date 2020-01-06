from django.urls import path

from customer.Views.Comment import PostCommentView
from administrator.Views.Articles import ArticleView
from customer.Views.Post import MakePostView
from customer.Views.SearchPost import SearchPostView

urlpatterns = [
    path('post/', MakePostView.as_view()),
    path('comment/', PostCommentView.as_view()),
    path('postsearch', SearchPostView.as_view()),
    path('article', ArticleView.as_view()),
]