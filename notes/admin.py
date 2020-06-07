from django.contrib import admin

from .models import Note

from guardian.admin import GuardedModelAdmin


class NoteAdmin(GuardedModelAdmin):
    list_display = ['title', 'body', 'creator', 'updated_at', 'created_at', 'id']
    search_fields = ['title', 'created_at']
    ordering = ['-updated_at']
    date_hierarchy = 'created_at'


admin.site.register(Note, NoteAdmin)
