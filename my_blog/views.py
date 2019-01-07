from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db.models import Count
from django.shortcuts import render, redirect
import logging
from django.conf import settings
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

from my_blog.forms import CommentForm, LoginForm, RegForm
from my_blog.models import Category, Article, Ad, Comment, User

logger = logging.getLogger('my_blog.views')

# Create your views here.
def global_settings(request):
    # 分类信息获取，作为导航
    category_list = Category.objects.all()[:1]
    # 广告数据
    ad_list = Ad.objects.all()
    # 文章归档
    # 1.获取到文章中的月份
    archive_list = Article.objects.distinct_date()

    # 获取文章评论数排行
    article_list_comment = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
    article_list_comment = [ Article.objects.get(pk=comment['article']) for comment in article_list_comment]

    # 获取文章浏览量排行
    article_list_click = Article.objects.all().order_by('click_count')[:10]

    # 获取文章推荐排行
    article_list_recommend = Article.objects.filter(is_recommend=True)[:10]
    SITE_NAME= settings.SITE_NAME
    SITE_DESC= settings.SITE_DESC
    WEIBO_SINA= settings.WEIBO_SINA
    WEIBO_TECENT= settings.WEIBO_TECENT
    PRO_RSS=settings.PRO_RSS
    PRO_EMAIL= settings.PRO_EMAIL
    MEDIA_URL= settings.MEDIA_URL
    SITE_URL = settings.SITE_URL
    return locals()
    # return {
    #     'category_list': category_list,
    #     'ad_list': ad_list,
    #     'archive_list':archive_list,
    #     'SITE_NAME' : settings.SITE_NAME,
    #     'SITE_DESC' : settings.SITE_DESC,
    #     'WEIBO_SINA' : settings.WEIBO_SINA,
    #     'WEIBO_TECENT' : settings.WEIBO_TECENT,
    #     'PRO_RSS' : settings.PRO_RSS,
    #     'PRO_EMAIL' : settings.PRO_EMAIL,
    #     'MEDIA_URL' : settings.MEDIA_URL,
    #     'article_list_comment':article_list_comment,
    #     'article_list_click':article_list_click,
    #     'article_list_recommend':article_list_recommend,
    #         }

def index(request):
    try:
        # 最新文章数据
        article_list = Article.objects.all()
        # 获取分页数据
        article_list = getPage(request,article_list)
        # return render(request, 'index.html', {'category_list': category_list,'article_list':article_list})
        return render(request, 'index.html', locals())
    except Exception as e:
        logger.error(e)

def archive(request):
    try:
        # 获取客户端提交的信息
        year = request.GET.get('year',None)
        month = request.GET.get('month',None)
        # 模糊查询该时间的文章
        article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)

        # 获取分页页面文章列表
        article_list = getPage(request,article_list)

    except Exception as e:
        logger.error(e)
    return render(request,'archive.html',locals())

# Common func of paginator
def getPage(request, query_set):
    paginator = Paginator(query_set, 2)
    try:
        page = int(request.GET.get('page', 1))
        query_set = paginator.page(page)
    except (EmptyPage,InvalidPage,PageNotAnInteger) as e:
        query_set = paginator.page(1)
    return query_set

# Details of article
# 文章详情
def article(request):
    try:
        # 获取文章id
        id = request.GET.get('id', None)
        try:
            # 获取文章信息
            article = Article.objects.get(pk=id)
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})

        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id} if request.user.is_authenticated() else{'article': id})
        # 获取评论信息
        comments = Comment.objects.filter(article=article).order_by('id')
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)
    except Exception as e:
        print(e)
        logger.error(e)
    return render(request, 'article.html', locals())


# 提交评论
def comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            #获取表单信息
            comment = Comment.objects.create(username=comment_form.cleaned_data["author"],
                                             email=comment_form.cleaned_data["email"],
                                             url=comment_form.cleaned_data["url"],
                                             content=comment_form.cleaned_data["comment"],
                                             article_id=comment_form.cleaned_data["article"],
                                             user=request.user if request.user.is_authenticated() else None)
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        # print(e)
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

# 注册
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                    email=reg_form.cleaned_data["email"],
                                    url=reg_form.cleaned_data["url"],
                                    password=make_password(reg_form.cleaned_data["password"]),)
                user.save()

                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())

# 登录
def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())

def category(request):
    try:
        # 先获取客户端提交的信息
        cid = request.GET.get('cid', None)
        try:
            category = Category.objects.get(pk=cid)
        except Category.DoesNotExist:
            return render(request, 'failure.html', {'reason': '分类不存在'})
        article_list = Article.objects.filter(category=category)
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'category.html', locals())