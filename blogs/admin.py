from django.contrib import admin

from blogs.models import Blog, Category

# Register your models here.

admin.site.register(Category)
admin.site.register(Blog)