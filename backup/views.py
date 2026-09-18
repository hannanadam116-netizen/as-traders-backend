import os

from django.conf import settings
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import BackupService


# ==========================================
# CREATE BACKUP
# ==========================================

class CreateBackupView(APIView):

    def post(self, request):

        result = BackupService.create_backup()

        return Response(
            result,
            status=status.HTTP_201_CREATED,
        )


# ==========================================
# LIST BACKUPS
# ==========================================

class BackupListView(APIView):

    def get(self, request):

        return Response(
            BackupService.list_backups()
        )


# ==========================================
# DOWNLOAD BACKUP
# ==========================================

class DownloadBackupView(APIView):

    def get(self, request, filename):

        path = os.path.join(
            settings.BASE_DIR,
            "backups",
            filename,
        )

        return FileResponse(
            open(path, "rb"),
            as_attachment=True,
            filename=filename,
        )


# ==========================================
# DELETE BACKUP
# ==========================================

class DeleteBackupView(APIView):

    def delete(self, request, filename):

        path = os.path.join(
            settings.BASE_DIR,
            "backups",
            filename,
        )

        if os.path.exists(path):

            os.remove(path)

            return Response({
                "success": True,
            })

        return Response(
            {
                "error": "Backup not found."
            },
            status=status.HTTP_404_NOT_FOUND,
        )
class RestoreBackupView(APIView):

    def post(self, request, filename):

        result = BackupService.restore_backup(
            filename,
        )

        return Response(result)