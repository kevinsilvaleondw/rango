
from django.contrib import admin
from rango.models import Category, Page, Car
from rango.models import UserProfile


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


admin.site.register(Category)
admin.site.register(Page, PageAdmin)
admin.site.register(Car)
admin.site.register(UserProfile)
