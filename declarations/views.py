from django.views.generic import ListView

from declarations.models import Office, year_list


class DeclarationListView(ListView):
    template_name = 'declaration_list_view.html'

    def get_queryset(self):
        return Office.objects.get(id=self.kwargs['id']).get_children()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = year_list
        return context

    class Meta:
        model = Office
