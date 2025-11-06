from poms.common.serializers import (
    ModelWithUserCodeSerializer,
)
from poms.provenance.models import Source, Provider, ProviderVersion, SourceVersion


class ProviderSerializer(ModelWithUserCodeSerializer):
    class Meta:
        model = Provider
        fields = [
            "id",
            "master_user",
            "user_code",
            "name",
            "short_name",
            "public_name",

        ]


class ProviderVersionSerializer(ModelWithUserCodeSerializer):
    class Meta:
        model = ProviderVersion
        fields = [
            "id",
            "master_user",
            "user_code",
            "name",
            "short_name",
            "public_name",
            "provider",

            "version_semantic",
            "version_calendar"

        ]


class SourceSerializer(ModelWithUserCodeSerializer):
    class Meta:
        model = Source
        fields = [
            "id",
            "master_user",
            "user_code",
            "name",
            "short_name",
            "public_name"
        ]


class SourceVersionSerializer(ModelWithUserCodeSerializer):
    class Meta:
        model = SourceVersion
        fields = [
            "id",
            "master_user",
            "user_code",
            "name",
            "short_name",
            "public_name",
            "source",

            "version_semantic",
            "version_calendar"
        ]
