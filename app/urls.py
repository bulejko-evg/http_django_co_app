from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import (
    path,
    include,
    re_path,
)


urlpatterns = [
    path("admin/", admin.site.urls),

    re_path(r"^i18n/", include("django.conf.urls.i18n")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# handler400 = "app.apps.company.views.error.error_400"
# handler404 = "app.apps.company.views.error.error_404"
# handler500 = "app.apps.company.views.error.error_500"
# handler403 = "app.apps.company.views.error.error_403"
