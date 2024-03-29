from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Task, Tag


class TaskManagerAdminSite(admin.AdminSite):
    pass


task_manager_admin_site = TaskManagerAdminSite(name="Task manager admin")


@admin.register(Tag, site=task_manager_admin_site)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Task, site=task_manager_admin_site)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(User, site=task_manager_admin_site)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("role", "date_of_birth", "phone",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("role", "date_of_birth", "phone",)}),)
