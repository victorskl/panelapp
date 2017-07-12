from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy

from .views import RedirectGeneView
from .views import RedirectPanelView
from .views import RedirectWebServices
from .views import RedirectGenePanelView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url="/", permanent=False)),
    url(r'^PanelApp/$', RedirectView.as_view(url="/", permanent=False)),
    url(r'^PanelApp/Genes$', RedirectView.as_view(url="/panels/genes/", permanent=False)),
    url(r'^PanelApp/Genes/(?P<gene_symbol>.*)$', RedirectGeneView.as_view()),
    url(r'^PanelApp/PanelBrowser$', RedirectView.as_view(url=reverse_lazy("panels:index"))),
    url(r'^PanelApp/EditPanel/(?P<old_pk>[a-z0-9]+)$', RedirectPanelView.as_view()),
    url(r'^PanelApp/GeneReview/(?P<old_pk>[a-z0-9]+)/(?P<gene_symbol>.*)$',
        RedirectGenePanelView.as_view()),
    url(r'^WebServices/(?P<ws>.*)$', RedirectWebServices.as_view()),
]