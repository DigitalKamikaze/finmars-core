from django.db import models
from django.utils.translation import gettext_lazy

from poms.common.models import NamedModel, TimeStampedModel
from poms.users.models import MasterUser


class Provider(NamedModel, TimeStampedModel):
    master_user = models.ForeignKey(
        MasterUser,
        related_name="providers",
        verbose_name=gettext_lazy("master user"),
        on_delete=models.CASCADE,
    )

    class Meta(NamedModel.Meta):
        verbose_name = gettext_lazy("provider")
        verbose_name_plural = gettext_lazy("providers")


class ProviderVersion(NamedModel, TimeStampedModel):
    master_user = models.ForeignKey(
        MasterUser,
        related_name="provider_versions",
        verbose_name=gettext_lazy("master user"),
        on_delete=models.CASCADE,
    )

    provider = models.ForeignKey(
        Provider,
        verbose_name=gettext_lazy("provider"),
        on_delete=models.CASCADE,
    )

    version_semantic = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=gettext_lazy("provider version semantic"),
        help_text=gettext_lazy("Semantic Version https://semver.org/"),
    )

    version_calendar = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=gettext_lazy("provider version semantic"),
        help_text=gettext_lazy("Calendar Version https://calver.org/"),
    )

    class Meta(NamedModel.Meta):
        verbose_name = gettext_lazy("provider version")
        verbose_name_plural = gettext_lazy("providers versions")


class Source(NamedModel, TimeStampedModel):
    master_user = models.ForeignKey(
        MasterUser,
        related_name="sources",
        verbose_name=gettext_lazy("master user"),
        on_delete=models.CASCADE,
    )

    class Meta(NamedModel.Meta):
        verbose_name = gettext_lazy("source")
        verbose_name_plural = gettext_lazy("sources")


class SourceVersion(NamedModel, TimeStampedModel):
    master_user = models.ForeignKey(
        MasterUser,
        related_name="source_versions",
        verbose_name=gettext_lazy("master user"),
        on_delete=models.CASCADE,
    )

    source = models.ForeignKey(
        Source,
        verbose_name=gettext_lazy("source"),
        on_delete=models.CASCADE,
    )

    version_semantic = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=gettext_lazy("source version semantic"),
        help_text=gettext_lazy("Semantic Version https://semver.org/"),
    )

    version_calendar = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=gettext_lazy("source version semantic"),
        help_text=gettext_lazy("Calendar Version https://calver.org/"),
    )

    class Meta(NamedModel.Meta):
        verbose_name = gettext_lazy("source")
        verbose_name_plural = gettext_lazy("sources")


class PlatformVersion(NamedModel, TimeStampedModel):
    master_user = models.ForeignKey(
        MasterUser,
        related_name="platform_versions",
        verbose_name=gettext_lazy("master user"),
        on_delete=models.CASCADE,
    )

    version_details = models.JSONField(
        default=dict,  # will create {}
        blank=True,
        verbose_name=gettext_lazy("version details"),
        help_text=gettext_lazy("JSON with all versions"),
    )

    # Example content of version_details
    # {
    #     "backend": "1.23.2-stable",
    #     "olap": "1.18.0-stable",
    #     "portal": "1.22.3-stable",
    #     "vue-portal": "1.22.6-stable",
    #     "workflow": "1.22.7-stable",
    #     "workflow-portal": "1.22.1-stable"
    # }


class ProvenanceModel(models.Model):
    provider = models.ForeignKey(
        "provenance.Provider",
        null=True,
        blank=True,
        verbose_name=gettext_lazy("provider"),
        on_delete=models.CASCADE,
    )

    provider_version = models.ForeignKey(
        "provenance.ProviderVersion",
        null=True,
        blank=True,
        verbose_name=gettext_lazy("provider_version"),
        on_delete=models.CASCADE,
    )

    source = models.ForeignKey(
        "provenance.Source",
        null=True,
        blank=True,
        verbose_name=gettext_lazy("source"),
        on_delete=models.CASCADE,
    )

    source_version = models.ForeignKey(
        "provenance.SourceVersion",
        null=True,
        blank=True,
        verbose_name=gettext_lazy("source_version"),
        on_delete=models.CASCADE,
    )

    platform_version = models.ForeignKey(
        "provenance.PlatformVersion",
        null=True,
        blank=True,
        verbose_name=gettext_lazy("platform version"),
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
