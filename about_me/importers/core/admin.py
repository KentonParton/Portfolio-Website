from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from about_me.importers.orders.models import Department


class DepartmentInline(admin.TabularInline):
    model = Department
    fields = ["warehouse", "driver"]
    can_delete = False
    verbose_name_plural = "Department"


class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    inlines = [
        DepartmentInline,
    ]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)