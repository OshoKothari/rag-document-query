import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ingestion import store_document_in_weaviate  # This is where you have the document ingestion logic

UPLOAD_DIR = "uploaded_files"

# Event handler class
class WatcherHandler(FileSystemEventHandler):
    def on_created(self, event):
        """Triggered when a new file is created (uploaded)."""
        if event.is_directory:
            return
        if event.event_type == 'created':
            # Get file path and type
            file_path = event.src_path
            file_type = file_path.split(".")[-1].lower()

            # Store document in Weaviate
            store_document_in_weaviate(file_path, file_type)
            print(f"New document {file_path} uploaded and stored in Weaviate.")

# Start monitoring the directory
def start_watcher():
    event_handler = WatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, path=UPLOAD_DIR, recursive=False)
    observer.start()

    print(f"Monitoring {UPLOAD_DIR} for new files...")
    
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_watcher()
