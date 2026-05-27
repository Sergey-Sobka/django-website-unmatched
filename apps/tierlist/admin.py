from django.contrib import admin

from .models import TierListEntry


@admin.register(TierListEntry)
class TierListEntryAdmin(admin.ModelAdmin):
    list_display = (
        'mode',
        'character',
        'tier',
        'updated_by',
        'updated_at',
    )

    list_filter = (
        'mode',
        'tier',
    )

    search_fields = (
        'character__name',
        'notes',
    )
