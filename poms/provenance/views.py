from poms.common.views import AbstractModelViewSet
from poms.provenance.filters import (
    PlatformVersionFilterSet,
    ProviderFilterSet,
    ProviderVersionFilterSet,
    SourceFilterSet,
    SourceVersionFilterSet,
)
from poms.provenance.models import PlatformVersion, Provider, ProviderVersion, Source, SourceVersion
from poms.provenance.serializers import (
    PlatformVersionSerializer,
    ProviderSerializer,
    ProviderVersionSerializer,
    SourceSerializer,
    SourceVersionSerializer,
)


class ProviderViewSet(AbstractModelViewSet):
    queryset = Provider.objects
    filter_backends = AbstractModelViewSet.filter_backends + []
    filterset_class = ProviderFilterSet
    serializer_class = ProviderSerializer
    ordering_fields = [
        "user_code",
        "name",
        "short_name",
        "public_name",
    ]


class ProviderVersionViewSet(AbstractModelViewSet):
    queryset = ProviderVersion.objects
    filter_backends = AbstractModelViewSet.filter_backends + []
    filterset_class = ProviderVersionFilterSet
    serializer_class = ProviderVersionSerializer
    ordering_fields = [
        "user_code",
        "name",
        "short_name",
        "public_name",
    ]


class SourceViewSet(AbstractModelViewSet):
    queryset = Source.objects
    filter_backends = AbstractModelViewSet.filter_backends + []
    filterset_class = SourceFilterSet
    serializer_class = SourceSerializer
    ordering_fields = [
        "user_code",
        "name",
        "short_name",
        "public_name",
    ]


class SourceVersionViewSet(AbstractModelViewSet):
    queryset = SourceVersion.objects
    filter_backends = AbstractModelViewSet.filter_backends + []
    filterset_class = SourceVersionFilterSet
    serializer_class = SourceVersionSerializer
    ordering_fields = [
        "user_code",
        "name",
        "short_name",
        "public_name",
    ]


class PlatformVersionViewSet(AbstractModelViewSet):
    queryset = PlatformVersion.objects
    filter_backends = AbstractModelViewSet.filter_backends + []
    filterset_class = PlatformVersionFilterSet
    serializer_class = PlatformVersionSerializer
    ordering_fields = [
        "user_code",
        "name",
        "short_name",
        "public_name",
    ]
