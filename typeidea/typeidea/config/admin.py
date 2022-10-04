from django.contrib import admin
from .models import Link, SideBar
# Register your models here.
from typeidea.custom_admin import custom_site

@admin.register(Link, site=custom_site)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'href', 'weight', 'owner', 'created_time']
    fields = ('title', 'href', 'status', 'weight')

    def save_model(self, request, obj, form, change) -> None:
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)


@admin.register(SideBar, site=custom_site)
class SideBarAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_type', 'content', 'status', 'owner']
    fields = ('title', 'display_type', 'content')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SideBarAdmin, self).save_model(request, obj, form, change)
