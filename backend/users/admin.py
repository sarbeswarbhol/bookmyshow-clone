from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.html import format_html

class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        'username', 'email', 'role', 'phone', 'is_staff', 'is_superuser', 'profile_pic_preview'
    )
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            'fields': (
                'role',
                'phone',
                'location',
                'date_of_birth',
                'profile_picture',
            )
        }),
    )

    # 👇 Add this block for admin "Add user" page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'phone',
                'password1',
                'password2',
                'role',
                'is_staff',
                'is_superuser',
                'location',
                'date_of_birth',
                'profile_picture',
            ),
        }),
    )

    def profile_pic_preview(self, obj):
        if obj.profile_picture:
            return format_html(f'<img src="{obj.profile_picture.url}" width="40" height="40" style="border-radius:50%;" />')
        return "—"

    profile_pic_preview.short_description = 'Profile'

    def save_model(self, request, obj, form, change):
        if obj.role == 'admin':
            obj.is_staff = True
            obj.is_superuser = True
        super().save_model(request, obj, form, change)


admin.site.register(User, CustomUserAdmin)