from django.shortcuts import render
from .models import Article, Category, BlogComment, Tag
from .forms import BlogCommentForm
from django.shortcuts import get_object_or_404, redirect, get_list_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# import markdown2
import re
import logging

# Create your views here.

logger = logging.getLogger(__name__)


class IndexView(ListView):
    template_name = 'blog/index.html'
    # 制定获取的model数据列表的名字
    context_object_name = "article_list"

    def get_queryset(self):
        """
        过滤数据，获取已发布文章列表，并转为html格式
        Returns:
        """
        article_list = Article.objects.filter(status='0')
        # for article in article_list:
        #     article.body = markdown2.markdown(article.body,)
        return article_list

    # 为上下文添加额外的变量，以便在模板中访问
    def get_context_data(self, **kwargs):
        category_list = Category.objects.all().order_by('name')
        for category in category_list:
            count = Article.objects.filter(category__name=category.name).count()
            category.count = count
        tag_list = Tag.objects.all().order_by('name')
        for tag in tag_list:
            count = Article.objects.filter(tags__name=tag.name).count()
            tag.count = count
        kwargs['category_list'] = category_list
        kwargs['tag_list'] = tag_list
        return super(IndexView, self).get_context_data(**kwargs)

class CategoryView(ListView):
    template_name = 'blog/index.html'
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(category=self.kwargs['cate_id'], status='0')
        # for article in article_list:
        #     article.body = markdown2.markdown(article.body,)
        return article_list

    def get_context_data(self, **kwargs):
        category_list = Category.objects.all().order_by('name')
        for category in category_list:
            count = Article.objects.filter(category__name=category.name).count()
            category.count = count
        tag_list = Tag.objects.all().order_by('name')
        for tag in tag_list:
            count = Article.objects.filter(tags__name=tag.name).count()
            tag.count = count
        kwargs['category_list'] = category_list
        kwargs['tag_list'] = tag_list
        name = get_object_or_404(Category, pk=self.kwargs['cate_id'])
        kwargs['cate_name'] = name

        return super(CategoryView, self).get_context_data(**kwargs)


class TagView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        """
        根据指定的标签名获得该标签下的全部文章
        """
        article_list = Article.objects.filter(tags=self.kwargs['tag_id'], status='0')
        # for article in article_list:
        #     article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        category_list = Category.objects.all().order_by('name')
        for category in category_list:
            count = Article.objects.filter(category__name=category.name).count()
            category.count = count
        tag_list = Tag.objects.all().order_by('name')
        for tag in tag_list:
            count = Article.objects.filter(tags__name=tag.name).count()
            tag.count = count
        kwargs['category_list'] = category_list
        kwargs['tag_list'] = tag_list
        name = get_object_or_404(Tag, pk=self.kwargs['tag_id'])
        kwargs['tag_name'] = name
        return super(TagView, self).get_context_data(**kwargs)


class ArticleDetailView(DetailView):
    """
    显示文章详情
    """
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = "article"

    # pk_url_kwarg用于接受来自url中的参数作为主键
    pk_url_kwarg = 'article_id'

    # 从数据库中获取id为pk_url_kwargs的对象
    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        # 点击一次阅读量增加一次
        obj.views += 1
        obj.save()
        # obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'],)
        return obj

    # 新增form到上下文
    def get_context_data(self, **kwargs):
        kwargs['comment_list'] = self.object.blogcomment_set.all()
        kwargs['form'] = BlogCommentForm()
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        return super(ArticleDetailView, self).get_context_data(**kwargs)



def CommentView(request, article_id):
    if request.method == 'POST':
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['user_name']
            body = form.cleaned_data['body']

            article = get_object_or_404(Article, pk=article_id)
            new_record = BlogComment(user_name=name,
                                 body=body,
                                article=article)
            new_record.save()
            return redirect('app:detail', article_id=article_id)


def blog_search(request,):
    search_for = request.GET['search_for']
    if search_for:
        results = []
        article_list = get_list_or_404(Article)
        category_list = get_list_or_404(Category)
        for article in article_list:
            if re.findall(search_for, article.title):
                results.append(article)
        # for article in results:
        #     article.body = markdown2.markdown(article.body, )
        tag_list = Tag.objects.all().order_by('name')
        context = {
            'article_list': results,
            'category_list': category_list,
            'tag_list': tag_list,
        }

        return render(request, 'blog/index.html', context)
    else:
        return redirect('app:index')

def about(request,):
    return render(request, 'blog/about.html')