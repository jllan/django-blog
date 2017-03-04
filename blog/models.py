from django.db import models

# Create your models here.

__all__ = [
    'Category',     # 归档
    'Article',      # 文章
    'Tag',          # 标签
    'Comment',      # 评论
    'Link'          # 友链
]


class Article(models.Model):
    STATUS = (
        ('0', '发布'),
        ('1', '草稿')
    )
    title = models.CharField(max_length=64, unique=True, verbose_name='标题')
    abstract = models.TextField(verbose_name='摘要')
    body = models.TextField(verbose_name='内容')
    # on_delete 当指向的表被删除时，将该项设为空
    category = models.ForeignKey('Category', verbose_name='分类', null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag', verbose_name='标签', blank=True)
    url = models.CharField(max_length=255, verbose_name='链接', unique=True)
    status = models.CharField(default='0', max_length=1, choices=STATUS, verbose_name='文章状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')

    class Meta:
        # Meta 包含一系列选项，这里的ordering表示排序, - 表示逆序
        # 即当从数据库中取出文章时，以文章最后修改时间逆向排序
        verbose_name = '文章(Article)'
        verbose_name_plural = verbose_name
        ordering = ['-last_modified_time']

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='类名')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')

    class Meta:
        verbose_name = '分类(Category)'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='标签名')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')

    class Meta:
        verbose_name = '标签(Tag)'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.name


class Comment(models.Model):
    user_name = models.CharField(max_length=64, verbose_name='评论者名字')
    content = models.TextField(verbose_name='评论内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    article = models.ForeignKey('Article', verbose_name='评论所属文章', on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:20]


class Link(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='友链名字')
    url = models.URLField(unique=True, verbose_name='友链地址')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加日期')

    class Meta:
        verbose_name = '友情链接(Links)'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name
