import os
import shutil
from django.core.management.base import BaseCommand

"""
NOTE:- Official Command
##? Run -> python -m compileall -f .
➡️ এটা পুরানো __pycache__ মুছে নতুন করে বানায়
➡️ Production-safe
➡️ Django-specific না, Python-wide

##! Custom Command
NOTE:- Cline all __pycache__ directories
##? Run -> python manage.py clear_pycache 

##*If Prodcution Server -> systemctl restart gunicorn
⚠️ SAFE, কিন্তু condition সহ

- এটা কী করে?
    i) সব __pycache__ directory delete করে
    ii).pyc ফাইল remove করে

- Production এ সমস্যা হবে?
👉 না, যদি এই দুইটা rule মানো

⚠️ Rule 1 — Running process
- Gunicorn/uWSGI already loaded code → problem হবে না
- নতুন request এ Python আবার .pyc বানাবে

⚠️ Rule 2 — Permission
- File permission ঠিক থাকতে হবে
- Read-only FS হলে error আসবে
"""

class Command(BaseCommand):
    help = "Remove all __pycache__ directories from project"

    def handle(self, *args, **options):
        base_dir = os.getcwd()
        removed = 0

        for root, dirs, files in os.walk(base_dir):
            if "__pycache__" in dirs:
                cache_path = os.path.join(root, "__pycache__")
                shutil.rmtree(cache_path)
                removed += 1
                self.stdout.write(f"🧹 Removed: {cache_path}")

        self.stdout.write(
            self.style.SUCCESS(f"✅ Total __pycache__ removed: {removed}")
        )
