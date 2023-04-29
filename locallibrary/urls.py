from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("catalog/", include("catalog.urls")),
    path("", RedirectView.as_view(url="catalog/")),  # permanent=True)),
    path("accounts/", include("django.contrib.auth.urls")),
    path("users/", include("users.urls")),
    path("api/", include("api.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
