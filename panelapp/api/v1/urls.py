from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .viewsets import PanelsViewSet
from .viewsets import ActivityViewSet
from .viewsets import GeneViewSet
from .viewsets import STRViewSet

router = routers.DefaultRouter()
router.register(r'panels', PanelsViewSet, base_name='panels')
router.register(r'activities', ActivityViewSet, base_name='activities')

genes_router = routers.NestedDefaultRouter(router, r'panels', lookup='panel')
genes_router.register(r'genes', GeneViewSet, base_name='panels-genes')

strs_router = routers.NestedDefaultRouter(router, r'panels', lookup='panel')
strs_router.register(r'strs', GeneViewSet, base_name='panels-strs')

app_name = 'apiv1'
urlpatterns = [
    path('', include(router.urls)),
    path('', include(genes_router.urls)),
    path('', include(strs_router.urls)),
]
