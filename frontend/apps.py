import sys
import threading
from django.apps import AppConfig


def start_poll_telegram():
    import time
    time.sleep(1)
    from frontend.management.commands.poll_telegram import Command
    cmd = Command()
    cmd.stdout = sys.stdout
    cmd.stderr = sys.stderr
    cmd.handle()


class FrontendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'frontend'

    def ready(self):
        if 'runserver' in sys.argv and not any('--nopoll' in a for a in sys.argv):
            thread = threading.Thread(target=start_poll_telegram, daemon=True)
            thread.start()
