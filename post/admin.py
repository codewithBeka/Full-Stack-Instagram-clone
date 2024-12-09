from django.contrib import admin

# Register your models here.
from post.models import Post, Tag, Follow, Stream

# Register your models here.
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Stream)