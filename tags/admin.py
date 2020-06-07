from django.contrib import admin

from tags.models import GuardedTag

from guardian.admin import GuardedModelAdmin


class GuardedTagAdmin(GuardedModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    ordering = ['name']


admin.site.register(GuardedTag, GuardedTagAdmin)
