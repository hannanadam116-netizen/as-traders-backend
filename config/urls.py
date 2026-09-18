"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    path("admin/", admin.site.urls),

    path("api/masters/", include("masters.urls")),

    path("api/", include("transactions.urls")),

    path("api/", include("purchases.urls")),

    path("api/", include("payments.urls")),

    path("api/", include("dashboard.urls")),

    path("api/reports/", include("reports.urls")),

    path("api/company/", include("company.urls")),

    path(
      "api/gst/",
      include("gst.urls"),
    ),

    path("api/ledger/", include("ledger.urls")),

    path("api/inventory/", include("inventory.urls")),

    path(
      "api/accounts/",
      include("accounts.urls"),
    ),
    path(
      "api/backup/",
      include("backup.urls"),
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
