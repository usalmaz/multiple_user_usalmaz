from django.contrib import admin
from .models import User, Profile, Post, Country

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Country)


admin.site.site_header = 'Welcome Scott!'
