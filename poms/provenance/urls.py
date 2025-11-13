from rest_framework import routers

import poms.provenance.views as provenance

router = routers.DefaultRouter()

router.register(
    r"provider",
    provenance.ProviderViewSet,
    "provider",
)
router.register(
    r"provider-version",
    provenance.ProviderVersionViewSet,
    "providerVersion",
)
router.register(
    r"source",
    provenance.SourceViewSet,
    "source",
)
router.register(
    r"source-version",
    provenance.SourceVersionViewSet,
    "sourceVersion",
)


router.register(
    r"platform-version",
    provenance.PlatformVersionViewSet,
    "platformVersion",
)
