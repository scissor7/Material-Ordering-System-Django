from django.contrib import admin
from rbac import models

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title','url', 'is_menu']
    list_editable = ['title','url', 'is_menu']
    list_display_links = None

admin.site.register(models.Permission,PermissionAdmin)


admin.site.register(models.Role)
admin.site.register(models.UserInfo)