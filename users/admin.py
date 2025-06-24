# 用户管理后台自定义
# 支持表格、头像预览、增删改查、积分调整、角色分配、导入导出

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import User
import admin_thumbnails
from django.utils.html import format_html

@admin_thumbnails.thumbnail('avatar')
class UserAdmin(ImportExportModelAdmin):
    """
    用户管理后台，支持头像缩略图、积分、角色、导入导出等
    """
    list_display = ('username', 'email', 'role', 'points', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_active', 'is_staff')
    actions = ['reset_password', 'add_points']
    readonly_fields = ('last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('权限', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('积分', {'fields': ('points',)}),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )

    def reset_password(self, request, queryset):
        for user in queryset:
            user.set_password('12345678')
            user.save()
        self.message_user(request, "选中用户密码已重置为12345678")
    reset_password.short_description = "重置密码为12345678"

    def add_points(self, request, queryset):
        for user in queryset:
            user.points += 10
            user.save()
        self.message_user(request, "选中用户积分已增加10分")
    add_points.short_description = "批量增加10积分"

admin.site.register(User, UserAdmin)
