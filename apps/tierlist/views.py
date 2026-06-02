from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


class TierListEntryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = TierListEntry
    form_class = TierListEntryForm
    template_name = 'tierlist/tier_entry_form.html'
    success_url = reverse_lazy('tierlist:tier-list')
    permission_required = 'tierlist.add_tierlistentry'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user

        return super().form_valid(form)


class TierListEntryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = TierListEntry
    form_class = TierListEntryForm
    template_name = 'tierlist/tier_entry_form.html'
    success_url = reverse_lazy('tierlist:tier-list')
    permission_required = 'tierlist.change_tierlistentry'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user

        return super().form_valid(form)
