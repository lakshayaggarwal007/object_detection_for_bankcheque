import threading
from django.apps import AppConfig

class ImageProcessingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'image_processing_app'

    def ready(self):
        from . import folder_watcher
        watcher_thread = threading.Thread(target=folder_watcher.start_watcher, daemon=True)
        watcher_thread.start()
