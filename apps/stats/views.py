from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from .forms import MatchRecordForm
from .models import MatchRecord
from .selectors import character_stats, match_list


class MatchRecordListView(ListView):
    template_name = 'stats/match_record_list.html'
    context_object_name = 'matches'
    paginate_by = 10

    def get_queryset(self):
        return match_list()


class MatchRecordCreateView(LoginRequiredMixin, CreateView):
    model = MatchRecord
    form_class = MatchRecordForm
    template_name = 'stats/match_record_form.html'
    success_url = reverse_lazy('stats:match-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user

        return super().form_valid(form)


class CharacterStatsView(TemplateView):
    template_name = 'stats/character_stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mode'] = self.request.GET.get('mode', '')
        context['modes'] = MatchRecord.Modes.choices
        context['stats'] = character_stats(
            mode=context['mode']
        )

        return context
