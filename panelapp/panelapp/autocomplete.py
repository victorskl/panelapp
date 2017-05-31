from django.db.models import Q
from dal_select2.views import Select2QuerySetView
from dal_select2.views import Select2ListView
from panels.models import Gene
from panels.models import Evidence


class GeneAutocomplete(Select2QuerySetView):
    def get_queryset(self):
        qs = Gene.objects.all()

        if self.q:
            qs = qs.filter(Q(gene_symbol__istartswith=self.q) | Q(gene_name__istartswith=self.q))

        return qs


class SourceAutocomplete(Select2ListView):
    def get_list(self):
        return Evidence.ALL_SOURCES
