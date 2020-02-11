from django.urls import path

from administrator.Views.AddArticleCategory import AddArticleCategoryView
from administrator.Views.AddStaticArticle import AddStaticArticleView
from administrator.Views.AddStaticCategory import AddStaticCategoryView
from .Views.Articles import ArticleView
from .Views.ImageUpload import ImageUploadView
from.Views.AdImageUpload import AdImageView

urlpatterns = [
    path('article/', ArticleView.as_view(), name="article"),
    path('image_upload', ImageUploadView.as_view(), name="image_upload"),
    path('ad_image', AdImageView.as_view(), name="ad_image"),
    path('staticCategory', AddStaticCategoryView.as_view(), name="add_static_category"),
    path('staticArticle', AddStaticArticleView.as_view(), name="add_static_article"),
    path('articleCategory', AddArticleCategoryView.as_view(), name="add_article_category"),
    # path('user_account/', UserAccountView.as_view()),
]