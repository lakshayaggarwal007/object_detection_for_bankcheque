import time
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from django.conf import settings
from image_processing_app.views import process_image_with_yolov8

class ImageHandler(FileSystemEventHandler):
    processed_files = set()  # Set to track processed files

    def on_created(self, event):
        # Check if the created file is an image (you can modify the extension check as needed)
        if event.is_directory or not event.src_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            return

        image_path = event.src_path
        image_name = os.path.basename(image_path).rsplit('.', 1)[0]

        # Avoid processing the same file twice
        if image_name in self.processed_files:
            return

        # Introduce a delay to ensure the file is fully written
        time.sleep(1)  # Adjust the sleep time as necessary

        # Process the new image using YOLO
        result = process_image_with_yolov8(image_path, image_name)

        # Save the result to the JSON file
        result_path = os.path.join(settings.MEDIA_ROOT, 'results.json')
        existing_data = {}
        if os.path.exists(result_path):
            with open(result_path, 'r') as f:
                existing_data = json.load(f)
        
        existing_data[image_name] = result
        with open(result_path, 'w') as f:
            json.dump(existing_data, f)

        # Mark the file as processed
        self.processed_files.add(image_name)

def start_watcher():
    images_folder = os.path.join(settings.BASE_DIR, 'images')
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path=images_folder, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_watcher()
