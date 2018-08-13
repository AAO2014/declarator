from django.shortcuts import render
from django.views.generic import ListView

from declarations.models import Office, Document


class DeclarationListView(ListView):
    template_name = 'declaration_list_view.html'

    def get_queryset(self):
        return Office.objects.get(id=self.kwargs['id']).get_ancestors()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['office_list'] = Office.objects.get(
            id=int(self.kwargs['id'])
        ).get_children()
        context['years'] = Document.objects.all().order_by('-income_year')\
            .distinct().values_list('income_year', flat=True)
        return context

    class Meta:
        model = Office
