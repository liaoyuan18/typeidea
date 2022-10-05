from django.shortcuts import render
# from django.http import HttpResponse

from config.models import SideBar
from .models import Tag, Post, Category
# Create your views here.


def post_list(request, category_id=None, tag_id=None):
    # content = 'post_list category_id={category_id},tag_id={tag_id}'.format(
    #     category_id=category_id, tag_id=tag_id)
    # return HttpResponse(content)
    tag = None
    category = None

    # if tag_id:
    #     try:
    #         tag = Tag.objects.get(id=tag_id)
    #     except Tag.DoesNotExist:
    #         post_list = []
    #     else:
    #         post_list = tag.post_set.filter(status=Post.STATUS_NARMAL)
    # else:
    #     post_list = Post.objects.filter(status=Post.STATUS_NARMAL)
    #     if category_id:
    #         try:
    #             category = Category.objects.get(id=category_id)
    #         except Category.DoesNotExist:
    #             category = None
    #         else:
    #             post_list = post_list.objects.filter(category_id=category_id)

    # 在model中设置以下静态方法后再次重构代码
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id=tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id=category_id)
    else:
        post_list = Post.latest_posts()
    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SideBar.get_all()
    }
    context.update(Category.get_navs())
    print(context)
    return render(request, 'blog/list.html', context=context)
    # return render(request, 'blog/list.html', context={'name': 'post_list'})


def post_detail(request, post_id):
    # return HttpResponse('detail')
    # return render(request, 'blog/detail.html', context={'name': 'post_detail'})
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    context = {'post': post, 'sidebars': SideBar.get_all()}
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context)
