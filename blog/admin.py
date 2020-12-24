from django.contrib import admin
from .models import Post, Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'status', 'publish', 'image')
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'pub_date', 'moderate')
    list_filter = ('post', 'pub_date')
    search_fields = ('author', 'content')
