from django.shortcuts import render
from django.views.generic import ListView

from declarations.models import Office


class DeclarationListView(ListView):
    template_name = 'declaration_list_view.html'

    def get_queryset(self):
        return Office.objects.get(id=self.kwargs['id']).get_ancestors()

    class Meta:
        model = Office