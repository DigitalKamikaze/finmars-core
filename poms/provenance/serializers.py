from rest_framework import serializers

from poms.common.serializers import (
    ModelMetaSerializer,
    ModelWithTimeStampSerializer,
    ModelWithUserCodeSerializer,
)
from poms.provenance.models import PlatformVersion, Provider, ProviderVersion, Source, SourceVersion
from poms.users.fields import MasterUserField


class ProviderSerializer(ModelWithUserCodeSerializer, ModelWithTimeStampSerializer, ModelMetaSerializer):
    master_user = MasterUserField()

    class Meta:
        model = Provider
        fields = ["id", "master_user", "user_code", "name", "short_name", "public_name", "notes"]


class ProviderVersionSerializer(ModelWithUserCodeSerializer, ModelWithTimeStampSerializer, ModelMetaSerializer):
    master_user = MasterUserField()

    class Meta:
        model = ProviderVersion
        fields = [
            "id",
            "master_user",
            "user_code",
            "name",
            "short_name",
            "public_name",
            "notes",
            "provider",
            "version_semantic",
            "version_calendar",
        ]


class SourceSerializer(ModelWithUserCodeSerializer, ModelWithTimeStampSerializer, ModelMetaSerializer):
    master_user = MasterUserField()

    class Meta:
        model = Source
        fields = ["id", "master_user", "user_code", "name", "short_name", "public_name", "notes"]


class SourceVersionSerializer(ModelWithUserCodeSerializer, ModelWithTimeStampSerializer, ModelMetaSerializer):
    master_user = MasterUserField()

    class Meta:
        model = SourceVersion
        fields = [
            "id",
            "master_user",
            "user_code",
            "name",
            "short_name",
            "public_name",
            "notes",
            "source",
            "version_semantic",
            "version_calendar",
        ]


class PlatformVersionSerializer(ModelWithUserCodeSerializer, ModelWithTimeStampSerializer, ModelMetaSerializer):
    master_user = MasterUserField()

    class Meta:
        model = PlatformVersion
        fields = [
            "id",
            "master_user",
            "user_code",
            "name",
            "short_name",
            "public_name",
            "notes",
            "version_details",
        ]


class ModelWithProvenanceSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["provider"] = serializers.PrimaryKeyRelatedField(
            queryset=Provider.objects.all(), allow_null=True, required=False
        )
        self.fields["provider_object"] = ProviderSerializer(source="provider", read_only=True)
        self.fields["provider_version"] = serializers.PrimaryKeyRelatedField(
            queryset=ProviderVersion.objects.all(), allow_null=True, required=False
        )
        self.fields["provider_version_object"] = ProviderVersionSerializer(source="provider_version", read_only=True)

        self.fields["source"] = serializers.PrimaryKeyRelatedField(
            queryset=Source.objects.all(), allow_null=True, required=False
        )
        self.fields["source_object"] = SourceSerializer(source="source", read_only=True)
        self.fields["source_version"] = serializers.PrimaryKeyRelatedField(
            queryset=SourceVersion.objects.all(), allow_null=True, required=False
        )
        self.fields["source_version_object"] = SourceVersionSerializer(source="source_version", read_only=True)

        self.fields["platform_version"] = serializers.PrimaryKeyRelatedField(
            queryset=PlatformVersion.objects.all(), allow_null=True, required=False
        )
        self.fields["platform_version_object"] = PlatformVersionSerializer(source="platform_version", read_only=True)

    def validate(self, data):
        return data
