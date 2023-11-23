from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import handler403, handler404, handler500
from locallibrary.views import view_403, view_404, view_500

urlpatterns = [
    path("admin/", admin.site.urls),
    # Apps
    path("catalog/", include("catalog.urls")),
    path("", RedirectView.as_view(url="catalog/")),  # permanent=True)),
    path("api/", include("api.urls")),
    # Users
    path("accounts/", include("django.contrib.auth.urls")),
    path("users/", include("users.urls")),
    path("api/users/", include("users.api.urls")),
    # Misc
    path('view-403/', view_403, name='view_403'),
    path('view-404/', view_404, name='view_404'),
    path('view-500/', view_500, name='view_500'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )

handler403 = view_403
handler404 = view_404
handler500 = view_500
