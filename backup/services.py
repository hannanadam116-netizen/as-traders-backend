import os
import subprocess
from datetime import datetime

from django.conf import settings
PG_DUMP = r"C:\Program Files\PostgreSQL\18\bin\pg_dump.exe"
PSQL = r"C:\Program Files\PostgreSQL\18\bin\psql.exe"

class BackupService:

    BACKUP_DIR = os.path.join(
        settings.BASE_DIR,
        "backups",
    )

    @classmethod
    def create_backup(cls):

        os.makedirs(
            cls.BACKUP_DIR,
            exist_ok=True,
        )

        filename = datetime.now().strftime(
            "backup_%Y%m%d_%H%M%S.sql"
        )

        filepath = os.path.join(
            cls.BACKUP_DIR,
            filename,
        )

        db = settings.DATABASES["default"]

        env = os.environ.copy()

        env["PGPASSWORD"] = db["PASSWORD"]

        command = [
            PG_DUMP,
            "-h",
            db["HOST"],
            "-p",
            db["PORT"],
            "-U",
            db["USER"],
            "-F",
            "p",
            "-f",
            filepath,
            db["NAME"],
        ]

        subprocess.run(
            command,
            check=True,
            env=env,
        )

        return {
            "success": True,
            "filename": filename,
        }

    @classmethod
    def list_backups(cls):

        os.makedirs(
            cls.BACKUP_DIR,
            exist_ok=True,
        )

        backups = []

        for file in sorted(
            os.listdir(cls.BACKUP_DIR),
            reverse=True,
        ):
            if file.endswith(".sql"):

                path = os.path.join(
                    cls.BACKUP_DIR,
                    file,
                )

                backups.append({
                    "name": file,
                    "size": os.path.getsize(path),
                    "created": datetime.fromtimestamp(
                        os.path.getmtime(path)
                    ),
                })

        return backups
    @classmethod
    def restore_backup(cls, filename):

        filepath = os.path.join(
            cls.BACKUP_DIR,
            filename,
        )

        if not os.path.exists(filepath):

            return {
                "success": False,
                "message": "Backup not found.",
            }

        db = settings.DATABASES["default"]

        env = os.environ.copy()

        env["PGPASSWORD"] = db["PASSWORD"]

        command = [
            PSQL,
            "-h",
            db["HOST"],
            "-p",
            db["PORT"],
            "-U",
            db["USER"],
            "-d",
            db["NAME"],
            "-f",
            filepath,
        ]

        subprocess.run(
            command,
            check=True,
            env=env,
        )

        return {
            "success": True,
            "message": "Database restored successfully.",
        }    