"""issue_tracker URL Configuration """

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("issue_tracker.apps.issues.urls")),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
