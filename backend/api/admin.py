from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin
# Register your models here.

class UserAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ("id",'username', 'first_name','phone_number')
    search_fields = ["id",'full_name','phone_number']

class UserProfileAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ("id",'full_name','mobile_number')
    search_fields = ["id", 'full_name','mobile_number']

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(FamilyDetails)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(User, UserAdmin)
admin.site.register(MatrimonialProfile)