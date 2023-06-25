from django.contrib import admin

from .models import Blog

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('user', 'id', 'title',),}

admin.site.register(Blog)