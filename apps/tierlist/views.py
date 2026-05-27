from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import TierListEntryForm
from .models import TierListEntry
from .selectors import tier_list


class TierListView(TemplateView):
    template_name = 'tierlist/tier_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mode'] = self.request.GET.get('mode', '1v1')
        context['modes'] = TierListEntry.Modes.choices
        context['tier_list'] = tier_list(
            mode=context['mode']
        )

        return context


class TierListEntryCreateView(LoginRequiredMixin, CreateView):
    model = TierListEntry
    form_class = TierListEntryForm
    template_name = 'tierlist/tier_entry_form.html'
    success_url = reverse_lazy('tierlist:tier-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('tierlist:tier-list')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.updated_by = self.request.user

        return super().form_valid(form)


class TierListEntryUpdateView(LoginRequiredMixin, UpdateView):
    model = TierListEntry
    form_class = TierListEntryForm
    template_name = 'tierlist/tier_entry_form.html'
    success_url = reverse_lazy('tierlist:tier-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('tierlist:tier-list')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.updated_by = self.request.user

        return super().form_valid(form)
