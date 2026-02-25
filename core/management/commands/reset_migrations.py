import os
import random
import shutil
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

"""
NOTE:- Delete all migrations and regenerate them
##? python manage.py reset_migrations
"""


EXCLUDE_DIRS = {
    "env",
    "venv",
    ".venv",
    "node_modules",
    ".git",
    "__pycache__",
}

class Command(BaseCommand):
    help = "Delete all app migrations safely (DEV ONLY)"

    def handle(self, *args, **options):

        if not settings.DEBUG:
            raise CommandError("❌ DEBUG=False. This command is DEV only.")

        # 🔢 Math confirmation
        a = random.randint(1, 9)
        b = random.randint(1, 9)

        self.stdout.write(self.style.WARNING(
            "⚠️ This will DELETE all APP migration files (not Django core)"
        ))
        self.stdout.write(f"👉 Confirm: {a} + {b} = ?")

        answer = input("Your answer: ").strip()
        if not answer.isdigit() or int(answer) != (a + b):
            raise CommandError("❌ Wrong answer. Aborted.")

        base_dir = os.getcwd()
        
        
        ##! Remove all __pycache__ directories from project
        removed = 0
        for root, dirs, files in os.walk(base_dir):
            if "__pycache__" in dirs:
                cache_path = os.path.join(root, "__pycache__")
                shutil.rmtree(cache_path)
                removed += 1
                self.stdout.write(f"🧹 Removed: {cache_path}")
        self.stdout.write(self.style.SUCCESS(f"✅ Total __pycache__ removed: {removed}"))

        ##! Delete all migrations
        removed = 0
        for root, dirs, files in os.walk(base_dir):
            # 🔒 Skip excluded dirs
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            if "migrations" in dirs:
                mig_dir = os.path.join(root, "migrations")

                # extra safety: must be inside Django app
                if not os.path.isfile(os.path.join(root, "apps.py")):
                    continue

                for file in os.listdir(mig_dir):
                    if file.endswith(".py") and file != "__init__.py":
                        os.remove(os.path.join(mig_dir, file))
                        removed += 1

        self.stdout.write(self.style.SUCCESS(f"🧹 Removed {removed} migration files safely"))
        
        ##! 🗄️ Optional: Delete db.sqlite3
        db_path = os.path.join(base_dir, "db.sqlite3")
        if os.path.exists(db_path):
            self.stdout.write(self.style.WARNING("\n⚠️ Do you want to DELETE db.sqlite3 ?"))
            self.stdout.write("Type 'yes' to confirm, anything else to skip")

            answer = input("Your choice [yes/no]: ").strip().lower()

            if answer in ("yes", "y"):
                os.remove(db_path)
                self.stdout.write(self.style.SUCCESS("🗑️ db.sqlite3 deleted successfully"))
            else:
                self.stdout.write(self.style.NOTICE("ℹ️ db.sqlite3 NOT deleted"))
        else:
            self.stdout.write(self.style.NOTICE("ℹ️ db.sqlite3 not found, skipping"))
        
        self.stdout.write("👉 Next steps:")
        self.stdout.write("   python manage.py makemigrations")
        self.stdout.write("   python manage.py migrate")
