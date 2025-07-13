from django.contrib import admin, messages
from .models import Movie, CastMember, Review

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


# 🔹 Movie Admin
@admin.register(Movie)
class MovieAdmin(SoftDeleteAdmin):
    list_display = ('title', 'language', 'genre', 'duration', 'rating', 'release_date', 'created_by', 'is_deleted')
    search_fields = ('title', 'genre', 'language', 'cast__name')
    list_filter = ('genre', 'language', 'release_date', 'is_deleted')
    autocomplete_fields = ['cast']

# 🔹 Cast Member Admin
@admin.register(CastMember)
class CastMemberAdmin(SoftDeleteAdmin):
    list_display = ('name', 'role', 'is_deleted')
    list_filter = ('role', 'is_deleted')
    search_fields = ('name',)

# 🔹 Review Admin
@admin.register(Review)
class ReviewAdmin(SoftDeleteAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at', 'is_deleted')
    list_filter = ('rating', 'created_at', 'is_deleted')
    search_fields = ('movie__title', 'user__username')
