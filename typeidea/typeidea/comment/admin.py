from django.contrib import admin
from .models import Comment
from django.utils.html import format_html
from django.urls import reverse

from typeidea.custom_admin import custom_site
# Register your models here.


@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'content', 'comment_of_post', 'status', 'website_link', 'email',
                    'created_time']

    def website_link(self, obj):
        return format_html('<a target="_blank" href="{website}">{website}</a>', website=obj.website)
    website_link.short_description = "网站"

    def comment_of_post(self, obj):
        return format_html('<a target="_blank" href="{url}" >{title}</a>',
                           url=reverse("admin:blog_post_change",
                                       args=(obj.target.id,)),
                           title=obj.target.title)
    comment_of_post.short_description = "文章链接"
