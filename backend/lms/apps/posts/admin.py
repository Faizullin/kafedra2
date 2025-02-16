from django.contrib import admin

from lms.core.loading import get_model
from utils.admin import BaseAdmin

Post = get_model("posts", "Post")
Category = get_model("posts", "Category")
Tag = get_model("posts", "Tag")


@admin.register(Post)
class PostAdmin(BaseAdmin):
    list_display = ('title', 'slug', 'publication_status',)
    list_filter = ("publication_status", 'category')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)


# @admin.register(PostComment)
# class PostCommentAdmin(BaseAdmin):
#     list_display = ('title', 'message',)
#     search_fields = ['message']


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ('title', 'slug',)
    search_fields = ['title', ]


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    list_display = ('title',)
    search_fields = ['title', ]
