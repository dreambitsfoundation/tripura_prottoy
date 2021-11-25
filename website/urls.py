from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signout', views.signout_user, name="signout"),
    path('joinus', views.user_login, name="join_us"),
    path('search', views.search, name="search"),
    # Administrator URLs
    path('adminDashboard', views.dashboard, name="admin_dashboard"),
    path('adminPostReview', views.post_review, name="admin_post_review"),
    path('adminUsers', views.users, name="admin_users"),
    path('adminWriteArticle', views.write_article, name="admin_write_article"),
    path('adminArticleList', views.articleList, name="admin_article_list"),
    path('adminEditArticle', views.edit_article, name="admin_edit_article"),
    path('adminArticleCategory', views.article_category, name="admin_article_category"),
    path('adminStaticArticleCategory', views.static_category, name="admin_static_article_category"),
    path('adminWriteStaticArticle', views.static_article, name="admin_static_article"),
    path('adminFacebookAccessToken', views.facebook_page_token, name="facebook_access_token"),
    path('adminManageAdImages', views.manage_ad_image, name="ad_image_manager"),
    path('adminManageAdVideos', views.manage_ad_video, name="ad_video_manager"),
    # Standard User URLs
    path('accountInfo', views.account_info, name="account_info"),
    path('changePassword', views.change_password, name="change_password"),
    path('activities', views.activities, name="activities"),
    path('newPost', views.new_post, name="new_post"),
    path('requestOrgAccess', views.org_user_access, name="org_access_rights"),
    # Common URLs
    path('postView', views.view_post, name="view_post"),
    path('articleView', views.view_article, name="view_article"),
    path('showStaticArticle', views.view_static_article, name="view_static_article"),
]
