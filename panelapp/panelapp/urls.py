##
## Copyright (c) 2016-2019 Genomics England Ltd.
##
## This file is part of PanelApp
## (see https://panelapp.genomicsengland.co.uk).
##
## Licensed to the Apache Software Foundation (ASF) under one
## or more contributor license agreements.  See the NOTICE file
## distributed with this work for additional information
## regarding copyright ownership.  The ASF licenses this file
## to you under the Apache License, Version 2.0 (the
## "License"); you may not use this file except in compliance
## with the License.  You may obtain a copy of the License at
##
##   http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing,
## software distributed under the License is distributed on an
## "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
## KIND, either express or implied.  See the License for the
## specific language governing permissions and limitations
## under the License.
##
"""panelapp URL Configuration

"""
from django.conf import settings
from django.conf.urls import url
from django.urls import path
from django.conf.urls import include
from django.contrib import admin
from .views import Homepage
from .views import HealthCheckView
from .views import VersionView
from .autocomplete import GeneAutocomplete
from .autocomplete import SourceAutocomplete
from .autocomplete import TagsAutocomplete
from .autocomplete import SimplePanelsAutocomplete
from .autocomplete import SimplePanelTypesAutocomplete


from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="PanelApp API",
        default_version="v1",
        description="PanelApp API",
        terms_of_service="https://panelapp.genomicsengland.co.uk/policies/terms/",
        contact=openapi.Contact(email="panelapp@genomicsengland.co.uk"),
    ),
    patterns=[path("api/", include("api.urls"))],  # exclude old webservices
    validators=["flex", "ssv"],
    public=True,
    permission_classes=(permissions.AllowAny,),  #  FIXME(Oleg) we need read only.
)


urlpatterns = [
    path("", Homepage.as_view(), name="home"),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("cognito/", include("cognito.urls", namespace="cognito")),
    path("panels/", include("panels.urls", namespace="panels")),
    path("crowdsourcing/", include("v1rewrites.urls", namespace="v1rewrites")),
    re_path(
        r"^api/docs(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=None),
        name="schema-json",
    ),
    re_path(
        r"^api/docs/$",
        schema_view.with_ui("swagger", cache_timeout=None),
        name="schema-swagger-ui",
    ),
    path("api/", include("api.urls", namespace="api")),
    path("WebServices/", include("webservices.urls", namespace="webservices")),
    path("markdownx/", include("markdownx.urls")),
    path(settings.ADMIN_URL, admin.site.urls),
    path("autocomplete/gene/", GeneAutocomplete.as_view(), name="autocomplete-gene"),
    path(
        "autocomplete/source/", SourceAutocomplete.as_view(), name="autocomplete-source"
    ),
    path("autocomplete/tags/", TagsAutocomplete.as_view(), name="autocomplete-tags"),
    path(
        "autocomplete/panels/simple/",
        SimplePanelsAutocomplete.as_view(),
        name="autocomplete-simple-panels",
    ),
    path(
        "autocomplete/panels/type/",
        SimplePanelTypesAutocomplete.as_view(),
        name="autocomplete-simple-panel-types",
    ),
    path("health_check/", HealthCheckView.as_view(), name="health_check"),
    path("version/", VersionView.as_view(), name="version"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns

    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
