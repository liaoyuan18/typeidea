import imp
from unicodedata import category
from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Category, Tag
from django.urls import reverse
# Register your models here.
from .adminform import PostAdminForm

from typeidea.custom_admin import custom_site

# 改造后的adminModel
from typeidea.base_admin import BaseOwnerAdmin
# 操作日志查看,引用
from django.contrib.admin.models import LogEntry


# 在同一页面编辑关联数据inline
class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]
    list_display = ('name', 'posts_count', 'status',
                    'is_nav', 'owner', 'created_time')
    fields = ('name', 'status', 'is_nav')
    # 自动设置owner保存

    # 显示每个分类的文章数量
    def posts_count(self, obj):
        return obj.post_set.count()
    posts_count.short_description = '文章数量'

# 因为在BaseOwnerAdmin中已经继承了，所以下方的代码不再需要
# 1.保存时自动添加保存user
# 2.获取列表时，只获取user自身的列表
#  自定义保存操作，设置user为当前用户
    # def save_model(self, request, obj, form, change) -> None:
    #     obj.owner = request.user
    #     return super().save_model(request, obj, form, change)

    # def get_queryset(self, request):
    #     return super().get_queryset(request).filter(owner=request.user)


@admin.register(Tag, site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')


# 过滤器 ，只显示当前用户的文章
class CategoryOwnerFilter(admin.SimpleListFilter):
    title = '分类过滤器'
    parameter_name = 'owner_category'

    # 侧边栏的filter筛选显示user自己创建的category进行筛选
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')
    # 列表显示，如果本筛选器传递了id过来，就显示筛选的结果

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm

    # operator 是自定义的
    list_display = ('title', 'category', 'status', 'operator', 'created_time')
    list_display_links = []
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                'title', 'category',
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            )
        }),
        ('额外信息', {
            'classes': ('wide',),
            'fields': ('tag',)
        }),
    )
    # 设置展示list中的自定义列

    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>', reverse('cus_admin:blog_post_change', args=(obj.id,)))
    operator.short_description = "操作"

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin, self).save_model(request, obj, form, change)

    # # 让显示的列表只显示自己写的文章

    # def get_queryset(self, request):
    #     qs = super(PostAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)

# 日志管理
@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user']
