from django.urls import path

from .views import (
    CreateBackupView,
    BackupListView,
    DownloadBackupView,
    DeleteBackupView,
    RestoreBackupView,
)

urlpatterns = [

    path(
        "create/",
        CreateBackupView.as_view(),
    ),

    path(
        "list/",
        BackupListView.as_view(),
    ),

    path(
        "download/<str:filename>/",
        DownloadBackupView.as_view(),
    ),

    path(
        "delete/<str:filename>/",
        DeleteBackupView.as_view(),
    ),

    path(
      "restore/<str:filename>/",
      RestoreBackupView.as_view(),
    ),
]