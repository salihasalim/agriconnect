from django.contrib import admin

from .models import CustomUser,Category,Tag


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Tag)
