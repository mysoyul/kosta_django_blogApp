from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'count_text']
    list_display_links = ['title']

    def count_text(self, post):
        return f'{len(post.text)}글자'

    count_text.short_description = 'text글자수'

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
