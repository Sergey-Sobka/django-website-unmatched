from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, ListView, UpdateView

from .forms import CardForm, CharacterForm, GameSetForm, MapForm
from .models import Card, Character, GameSet, Map
from .selectors import (
    character_get_by_slug,
    character_list,
    game_set_get_by_slug,
    game_set_list,
    map_get_by_slug,
    map_list,
)


class GameSetListView(ListView):
    template_name = 'wiki/game_set_list.html'
    context_object_name = 'game_sets'
    paginate_by = 9

    def get_queryset(self):
        return game_set_list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['query_params'] = query_params.urlencode()

        return context


class GameSetDetailView(DetailView):
    template_name = 'wiki/game_set_detail.html'
    context_object_name = 'game_set'

    def get_object(self, queryset=None):
        return game_set_get_by_slug(
            slug=self.kwargs['slug']
        )


class EditorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff


class GameSetUpdateView(EditorRequiredMixin, UpdateView):
    model = GameSet
    form_class = GameSetForm
    template_name = 'wiki/object_form.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class MapListView(ListView):
    template_name = 'wiki/map_list.html'
    context_object_name = 'maps'
    paginate_by = 9

    def get_queryset(self):
        return map_list(
            game_set=self.request.GET.get('game_set', '')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_sets'] = game_set_list()
        context['selected_game_set'] = self.request.GET.get('game_set', '')
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['query_params'] = query_params.urlencode()

        return context


class MapDetailView(DetailView):
    template_name = 'wiki/map_detail.html'
    context_object_name = 'map'

    def get_object(self, queryset=None):
        return map_get_by_slug(
            slug=self.kwargs['slug']
        )


class MapUpdateView(EditorRequiredMixin, UpdateView):
    model = Map
    form_class = MapForm
    template_name = 'wiki/object_form.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class CharacterListView(ListView):
    template_name = 'wiki/character_list.html'
    context_object_name = 'characters'
    paginate_by = 9

    def get_queryset(self):
        return character_list(
            search=self.request.GET.get('q', ''),
            attack_type=self.request.GET.get('attack_type', ''),
            game_set=self.request.GET.get('game_set', ''),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q', '')
        context['selected_attack_type'] = self.request.GET.get('attack_type', '')
        context['selected_game_set'] = self.request.GET.get('game_set', '')
        context['attack_types'] = Character.AttackTypes.choices
        context['game_sets'] = game_set_list()
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['query_params'] = query_params.urlencode()

        return context


class CharacterDetailView(DetailView):
    template_name = 'wiki/character_detail.html'
    context_object_name = 'character'

    def get_object(self, queryset=None):
        return character_get_by_slug(
            slug=self.kwargs['slug']
        )


class CharacterUpdateView(EditorRequiredMixin, UpdateView):
    model = Character
    form_class = CharacterForm
    template_name = 'wiki/object_form.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class CardUpdateView(EditorRequiredMixin, UpdateView):
    model = Card
    form_class = CardForm
    template_name = 'wiki/object_form.html'

    def get_success_url(self):
        return self.object.character.get_absolute_url()
