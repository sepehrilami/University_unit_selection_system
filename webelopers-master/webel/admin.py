from django.contrib import admin

from .models import Contact, Course, UserAvatar

# Register your models here.
admin.site.register(Contact)
admin.site.register(Course)
admin.site.register(UserAvatar)