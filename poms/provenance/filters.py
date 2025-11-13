from django_filters.rest_framework import FilterSet

from poms.common.filters import (
    CharFilter,
    NoOpFilter,
)
from poms.provenance.models import PlatformVersion, Provider, ProviderVersion, Source, SourceVersion


class ProviderFilterSet(FilterSet):
    id = NoOpFilter()
    user_code = CharFilter()
    name = CharFilter()
    short_name = CharFilter()
    public_name = CharFilter()

    class Meta:
        model = Provider
        fields = []


class ProviderVersionFilterSet(FilterSet):
    id = NoOpFilter()
    user_code = CharFilter()
    name = CharFilter()
    short_name = CharFilter()
    public_name = CharFilter()

    class Meta:
        model = ProviderVersion
        fields = []


class SourceFilterSet(FilterSet):
    id = NoOpFilter()
    user_code = CharFilter()
    name = CharFilter()
    short_name = CharFilter()
    public_name = CharFilter()

    class Meta:
        model = Source
        fields = []


class SourceVersionFilterSet(FilterSet):
    id = NoOpFilter()
    user_code = CharFilter()
    name = CharFilter()
    short_name = CharFilter()
    public_name = CharFilter()

    class Meta:
        model = SourceVersion
        fields = []


class PlatformVersionFilterSet(FilterSet):
    id = NoOpFilter()
    user_code = CharFilter()
    name = CharFilter()
    short_name = CharFilter()
    public_name = CharFilter()

    class Meta:
        model = PlatformVersion
        fields = []
