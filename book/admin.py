from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('subject', 'owner', 'kind', 'tag', 'date_posted')
    list_filter = ('tag', 'date_posted')
    search_fields = ('subject', 'content', 'owner__username')
    filter_horizontal = ('shared_with',)
