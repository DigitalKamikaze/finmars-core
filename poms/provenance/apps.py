from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class ProvenanceConfig(AppConfig):
    name = "poms.provenance"
    verbose_name = gettext_lazy("Provenance")
