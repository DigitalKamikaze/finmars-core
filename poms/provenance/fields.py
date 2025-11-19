from poms.common.fields import PrimaryKeyRelatedFilteredField
from poms.provenance.models import PlatformVersion, Provider, ProviderVersion, Source, SourceVersion


class ProviderField(PrimaryKeyRelatedFilteredField):
    queryset = Provider.objects


class ProviderVersionField(PrimaryKeyRelatedFilteredField):
    queryset = ProviderVersion.objects


class SourceField(PrimaryKeyRelatedFilteredField):
    queryset = Source.objects


class SourceVersionField(PrimaryKeyRelatedFilteredField):
    queryset = SourceVersion.objects


class PlatformVersionField(PrimaryKeyRelatedFilteredField):
    queryset = PlatformVersion.objects
