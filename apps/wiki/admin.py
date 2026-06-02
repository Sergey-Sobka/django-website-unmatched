from django.contrib import admin

from .models import Card, Character, GameSet, Map, Sidekick


class SidekickInline(admin.TabularInline):
    model = Sidekick
    extra = 0


class CardInline(admin.TabularInline):
    model = Card
    extra = 0


@admin.register(GameSet)
class GameSetAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'release_year',
        'bgg_link',
    )

    search_fields = (
        'name',
    )

    prepopulated_fields = {
        'slug': (
            'name',
        )
    }

    list_filter = (
        'release_year',
    )


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'game_set',
        'health',
        'movement',
        'attack_type',
    )

    list_filter = (
        'attack_type',
        'game_set',
    )

    search_fields = (
        'name',
        'subtitle',
    )

    prepopulated_fields = {
        'slug': (
            'name',
        )
    }

    inlines = (
        SidekickInline,
        CardInline,
    )


@admin.register(Sidekick)
class SidekickAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'character',
        'count',
        'health',
    )

    search_fields = (
        'name',
        'character__name',
    )


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'character',
        'card_type',
        'quantity',
        'value',
        'boost',
    )

    list_filter = (
        'card_type',
        'character',
    )

    search_fields = (
        'name',
        'character__name',
        'text',
    )


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'game_set',
        'players_count',
        'spaces_count',
        'zone_count',
    )

    list_filter = (
        'game_set',
        'players_count',
    )

    search_fields = (
        'name',
        'description',
    )

    prepopulated_fields = {
        'slug': (
            'name',
        )
    }
