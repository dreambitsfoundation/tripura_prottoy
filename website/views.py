from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.middleware import csrf
from django.shortcuts import render
import random
from django.db.models import Q
from django.db.models import Count

from django.contrib.auth import logout
# Create your views here.
from authentication.Decorators.AuthorizationValidator import login_required, admin_only, admin_only_route, \
    parse_user_profile
from administrator.models import AdVideoModel
from customer.Models import PostModel, CommentModel
from administrator.Models import ArticlesModel, ArticleCategoryModel, StaticCategoryModel, StaticArticleModel, AdImageModel
from authentication.models import User
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils import timezone



def get_or_cache(key: str, query):
    try:
        q = cache.get(key)
        print(q)
        if not q:
            q = query
            print("Reading from DB")
            cache.set(key, q, 60 * 15)
        else:
            print("Reading from cache")
    except:
        q = query
    return q


@parse_user_profile
def index(request):
    # print(csrf.get_token(request))
    # print(csrf.CsrfViewMiddleware().process_request(request))
    #static_cat = StaticCategoryModel.objects.filter(head_category = True)
    #all_posts = PostModel.objects.filter(approved=True).order_by('-id')[:10]
    article_categories = get_or_cache("article_category", ArticleCategoryModel.objects.all())
    parent_articles = get_or_cache("parent_articles", ArticleCategoryModel.objects.filter(parent_category = True))
    all_articles = get_or_cache("all_articles", ArticlesModel.objects.filter(published_on__gte=datetime.now() - timedelta(days=90)))
    mostly_viewed = get_or_cache("mostly_viewed", all_articles.order_by('-views')[:10])
    article = []
    print(article_categories.count())
    for a in article_categories:
        recent_articles = get_or_cache(f"recent_articles_{a.name}", all_articles.filter(category = a).order_by('-id')[:10])
        #background = colors[random.randrange(0, len(colors))]
        for r in recent_articles:
            r.images = r.generate_all_image_urls()
        article.append({
            "name": a.name,
            "articles": recent_articles
        })
    latest_articles = get_or_cache("latest_articles", all_articles.order_by('-published_on')[:10])
    for r in latest_articles:
            r.images = r.generate_all_image_urls()
    return render(request, "index_new.html", context={
        #"posts": all_posts,
        "articles": article,
        #"menu": static_cat,
        "article_menu": parent_articles,
        "latest_articles": latest_articles,
        "ad_image": {
            "tall_ad_images": get_or_cache("tall_ad_images", AdImageModel.objects.filter(tall_image_id__isnull=False).order_by('-id')[:8]),
            "wide_ad_images": get_or_cache("wide_ad_image", AdImageModel.objects.filter(wide_image_id__isnull=False).order_by('-id')[:8]),
            "tender_ad_images": get_or_cache("tender_ad_image", AdImageModel.objects.filter(tender_image_id__isnull=False).order_by('-id')[:8]),
        },
        "ad_videos": AdVideoModel.objects.all()[:5],
        "mostly_viewed": mostly_viewed,
        }
    )


def user_login(request):
    try:
        return render(request, "login.html")
    except:
        raise

""" User Account Related Views """
@login_required
def account_info(request):
    if request.user.is_administrator():
        return HttpResponseRedirect("adminDashboard")
    return render(request, "customer/account_info.html", context={"user": request.user, "page_title": "Account Info"})


@login_required
def activities(request):
    return render(request, "customer/activities.html", context={"user": request.user, "page_title": "Account Activities"})


@login_required
def new_post(request):
    return render(request, "customer/new_post.html", context={"user": request.user, "page_title": "New Post"})


@login_required
def change_password(request):
    return render(request, "customer/change_password.html", context={"page_title": "Change Password"})


@login_required
def org_user_access(request):
    return render(request, "customer/org_access_request.html", context={"page_title": "Organisation Access Request"})


def signout_user(request):
    logout(request)
    response = HttpResponseRedirect("/")
    response.delete_cookie("HTTP_AUTHORIZATION")
    return response


""" Administrator Account Related Views """
@login_required
@admin_only_route
def dashboard(request):
    if request.user.is_standard_user():
        return HttpResponseRedirect("accountInfo")
    queryset = User.objects.values('state').annotate(count = Count('state'))
    population = {
        "label" : [],
        "data": []
    }
    for q in queryset:
        population["label"].append(q["state"])
        population["data"].append(q["count"])
    queryset = PostModel.objects.values('organisation').annotate(count = Count('organisation'))
    complaints = {
        "label" : [],
        "data": []
    }
    for q in queryset:
        complaints["label"].append(q["organisation"])
        complaints["data"].append(q["count"])
    queryset = ArticlesModel.objects.values('category__name').annotate(count = Count('category'))
    articles = {
        "label" : [],
        "data": []
    }
    for q in queryset:
        if q["category__name"] != None:
            articles["label"].append(q["category__name"])
            articles["data"].append(q["count"])
    return render(request, "admin/dashboard.html", context={
        "user": request.user, 
        "page_title": "Site Details", 
        "locations": population, 
        "complaints": complaints,
        "articles": articles
        })


@login_required
@admin_only_route
def post_review(request):
    pending_posts = PostModel.objects.filter(pending_for_screening=True)
    return render(
        request,
        "admin/postreview.html",
        context={
            "user": request.user,
            "page_title": "Review New Post",
            "posts": pending_posts
        }
    )


@login_required
@admin_only_route
def write_article(request):
    categories = ArticleCategoryModel.objects.all()
    return render(
        request,
        "admin/write_article.html",
        context={"page_title": "New Article", "categories": categories}
    )


@login_required
@admin_only_route
def users(request):
    return render(request, "admin/users.html", context={"user": request.user, "page_title": "All Active Users"})


@login_required
@admin_only_route
def article_category(request):
    articles = ArticleCategoryModel.objects.all()
    parent_categories = ArticleCategoryModel.objects.filter(parent_category = True)

    return render(
        request,
        "admin/articleCategory.html",
        context={
            "user": request.user,
            "page_title": "Article Category",
            "parent_categories": parent_categories,
            "articles": articles
        }
    )


@login_required
@admin_only_route
def static_category(request):
    categories = StaticCategoryModel.objects.filter(head_category = True)
    return render(
        request,
        "admin/staticArticleCategory.html",
        context={
            "user": request.user,
            "page_title": "Static Article Category",
            "categories": categories
        }
    )

@login_required
@admin_only_route
def static_article(request):
    categories = StaticCategoryModel.objects.all()
    articles = StaticArticleModel.objects.all()
    return render(
        request,
        "admin/staticArticle.html",
        context={
            "user": request.user,
            "page_title": "Write Static Article",
            "categories": categories,
            "article": articles
        }
    )

@login_required
@admin_only_route
def facebook_page_token(request):
    return render(request, 'admin/add_facebook_page.html', {})

@login_required
@admin_only_route
def articleList(request):
    if request.method == "GET":
        articles = ArticlesModel.objects.all().order_by('-published_on')
        return render(request, 'admin/article_list.html', {"articles": articles})

@login_required
@admin_only_route
def edit_article(request):
    if request.method == "GET":
        id = int(request.GET.get("id", None))
        categories = ArticleCategoryModel.objects.all()
        if id is not None:
            articles = ArticlesModel.objects.filter(id=id)
            if len(articles):
                article = articles[0]
            return render(request, 'admin/write_article.html', {"article": article, "categories": categories})
        return HttpResponseRedirect("/adminArticleList")

@login_required
@admin_only
def manage_ad_image(request):
    tall_ad_images = AdImageModel.objects.filter(tall_image_id__isnull=False)
    wide_ad_images = AdImageModel.objects.filter(wide_image_id__isnull=False)
    tender_images = AdImageModel.objects.filter(tender_image_id__isnull=False)
    # if ad_image:
    #     ad_image = ad_image[0]
    # else:
    #     ad_image = None
    return render(request, 'admin/add_ad_image.html', {
        "title": "Manage Ads",
        "tall_ad_images": tall_ad_images,
        "wide_ad_images": wide_ad_images,
        "tender_images": tender_images
    })


@login_required
@admin_only
def manage_ad_video(request):
    ad_videos = AdVideoModel.objects.all()
    return render(request, 'admin/add_ad_video.html', {"title": "Manage Ad Videos", "videos":ad_videos})

""" Common Views """


def view_post(request):
    try:
        post_id = request.GET['id']
        post = PostModel.objects.get(id=int(post_id))
        if not post.approved:
            post = None
            comments = None
        else:
            comments = CommentModel.objects.filter(post=post, head_comment=True).order_by("-last_updated")
    except:
        post = None
        comments = None
    return render(
        request,
        "postView.html",
        context={
            "post": post,
            "comments": comments,
            "user": request.user,
            "page_title": "Post View"
        }
    )

def view_static_article(request):
    try:
        post_id = request.GET['id']
        post = StaticArticleModel.objects.get(id=int(post_id))
    except:
        post = None
    return render(
        request,
        "staticArticleView.html",
        context={
            "post": post,
            "user": request.user,
            "page_title": "Article View"
        }
    )

def view_article(request):
    try:
        article_id = request.GET['id']
        article = ArticlesModel.objects.get(id=int(article_id))
        comments = CommentModel.objects.filter(article = article, head_comment=True).order_by("-last_updated")
        # For navigation bar
        article_categories = ArticleCategoryModel.objects.all()
    except:
        article = None
        comments = None
        article_categories = []
    if article is not None:
        article.add_one_view()
        article.save()
    latest_articles = ArticlesModel.objects.all().order_by('-published_on')[:10]
    ad_image = AdImageModel.objects.filter(id=1)
    if len(ad_image) > 0:
        ad_image = ad_image[0]
    else:
        ad_image = None
    return render(
        request,
        "articleViewNew.html",
        context={
            "latest_articles": latest_articles,
            "article": article,
            "categories": [{"name": a.name} for a in article_categories],
            "comments": comments,
            "user": request.user,
            "page_title": "Article View",
            "images": article.generate_all_image_urls() if article else None,
            "ad_image": {
                "tall_ad_images": AdImageModel.objects.filter(tall_image_id__isnull=False).order_by('-id')[:8],
                "wide_ad_images": AdImageModel.objects.filter(wide_image_id__isnull=False).order_by('-id')[:8],
                "tender_ad_images": AdImageModel.objects.filter(tender_image_id__isnull=False).order_by('-id')[:8],
            },
        }
    )


def search(request):
    q = None
    search_type = "QUERY"  # Possible Values QUERY, ARCHIVE, CATEGORY
    results = 0
    articles = list()
    static_articles = list()
    archive_search_date = None
    try:
        search_type = request.GET.get('type', "QUERY")
        query = request.GET.get('q', None)
        category_id = request.GET.get('cat', None)
        if query and len(query) < 4:
            q = query
            raise Exception('Invalid Argument')
        archive_search_date = request.GET.get("search-date", None)
        if archive_search_date:
            archive_search_date = datetime.fromisoformat(archive_search_date)

        if category_id:
            categories = ArticleCategoryModel.objects.filter(id=category_id)
            if categories.count():
                q = categories[0].name
            else:
                raise Exception("Category not found.")

        if query:
            articles = ArticlesModel.objects.filter(Q(title__icontains=query)|Q(body__icontains=query)|Q(category__name=query)).distinct().order_by('-published_on')[:10]
            posts = PostModel.objects.filter(Q(title__icontains=query)|Q(body__icontains=query)|Q(organisation__icontains=query), approved=True).distinct()
            static_articles = StaticArticleModel.objects.filter(Q(title__icontains=query)|Q(content__icontains=query)).distinct()
            comments = CommentModel.objects.filter(text__icontains=query).order_by("-last_updated")
            results = articles.count() + posts.count() + static_articles.count() + comments.count()

        if category_id:
            articles = ArticlesModel.objects.filter(category__id=category_id, published_on__date=timezone.now().date())\
                .distinct().order_by('-published_on')
            results = articles.count()
            posts = None
            static_articles = None
            comments = None
            query = q
            search_type = "CATEGORY"

        if archive_search_date:
            articles = ArticlesModel.objects.filter(published_on__date=archive_search_date.date()) \
                .distinct().order_by('-published_on')
            results = articles.count()
            posts = None
            static_articles = None
            comments = None
            query = q
            search_type = "ARCHIVE"

    except Exception as e:
        raise e
        articles = None
        posts = None
        static_articles = None
        comments = None
        query = q
    return render(
        request,
        "search.html",
        context={
            "results": results,
            "articles": articles,
            "posts": list(),
            "static_articles": static_articles,
            "comments": list(),
            "user": request.user,
            "page_title": "Search",
            "query": query,
            "search_type": search_type,
            "archive_search_date": archive_search_date,
        }
    )