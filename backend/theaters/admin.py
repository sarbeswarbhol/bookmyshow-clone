from django.contrib import admin, messages
from .models import Show, Theater

# 🔹 Generic SoftDeleteAdmin base class
class SoftDeleteAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return self.model.all_objects.all()

    list_filter = ('is_deleted',)
    actions = ['restore_objects']

    def get_readonly_fields(self, request, obj=None):
        # Allow only superusers to edit is_deleted
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return super().get_readonly_fields(request, obj) + ('is_deleted',)

    @admin.action(description="Restore selected soft-deleted items")
    def restore_objects(self, request, queryset):
        restored = queryset.update(is_deleted=False)
        self.message_user(request, f"{restored} item(s) successfully restored.", messages.SUCCESS)
        if not restored:
            self.message_user(request, "No items were restored.", messages.WARNING)


# 🔹 Show Admin with Soft Delete Support
@admin.register(Show)
class ShowAdmin(SoftDeleteAdmin):
    list_display = ('movie', 'theater', 'show_time', 'created_by', 'is_deleted')
    list_filter = ('show_time', 'theater', 'movie', 'is_deleted')
    search_fields = ('movie__title', 'theater__name')


# 🔹 Theater Admin with Soft Delete Support
@admin.register(Theater)
class TheaterAdmin(SoftDeleteAdmin):
    list_display = ('name', 'location', 'capacity', 'created_by', 'is_deleted')
    search_fields = ('name', 'location')
    list_filter = ('location', 'is_deleted')
    prepopulated_fields = {"slug": ("name",)}