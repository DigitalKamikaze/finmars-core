from django.contrib import admin

from poms.common.admin import ClassModelAdmin
from poms.provenance.models import PlatformVersion, Provider, ProviderVersion, Source, SourceVersion

admin.site.register(Provider, ClassModelAdmin)
admin.site.register(ProviderVersion, ClassModelAdmin)
admin.site.register(Source, ClassModelAdmin)
admin.site.register(SourceVersion, ClassModelAdmin)
admin.site.register(PlatformVersion, ClassModelAdmin)
