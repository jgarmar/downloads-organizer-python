# downloads_organizer.py
# Automatically organizes files in the downloads folder after 24 hours
# Classifies files into appropriate folders based on their extensions

import os
import time
import shutil
import logging
import signal
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta

# Logging configuration
logging.basicConfig(
    filename='downloads_organizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Dictionary of extensions by category
EXTENSIONS = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico'],
    'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp'],
    'documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.ppt', '.pptx', '.csv', '.odt'],
    'music': ['.mp3', '.wav', '.flac', '.m4a', '.ogg', '.midi', '.aac', '.wma'],
    'programs': ['.exe', '.msi', '.app', '.bat', '.cmd', '.py', '.jar', '.dll'],
    'compressed': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso'],
    'others': []  # For files that don't match any category
}

class FileOrganizer(FileSystemEventHandler):
    def __init__(self, downloads_path):
        self.downloads_path = downloads_path
        self.pending_files = {}
        logging.info(f"Organizer started. Monitoring: {downloads_path}")
        self.process_existing_files()

    def process_existing_files(self):
        """Process files that already exist in the downloads folder"""
        logging.info("Processing existing files...")
        downloads_dir = Path(self.downloads_path)
        for file_path in downloads_dir.glob('*'):
            if file_path.is_file():
                # Add file to pending with its actual creation time
                creation_time = datetime.fromtimestamp(file_path.stat().st_ctime)
                self.pending_files[str(file_path)] = creation_time
                logging.info(f"Added existing file to queue: {file_path.name}")

    def on_created(self, event):
        # Executes when a new file is detected
        if not event.is_directory:
            file_path = event.src_path
            self.pending_files[file_path] = datetime.now()
            logging.info(f"New file detected: {os.path.basename(file_path)}")

    def process_pending_files(self):
        # Process files that have been pending for 24 hours
        current_time = datetime.now()
        files_to_remove = []

        for file_path, creation_time in self.pending_files.items():
            if current_time - creation_time >= timedelta(hours=24):
                self.organize_file(file_path)
                files_to_remove.append(file_path)

        # Clean up processed files list
        for file_path in files_to_remove:
            del self.pending_files[file_path]

    def organize_file(self, file_path):
        try:
            file = Path(file_path)
            if not file.exists():
                return

            # Determine category based on extension
            category = 'others'
            for cat, extensions in EXTENSIONS.items():
                if file.suffix.lower() in extensions:
                    category = cat
                    break

            # Create destination folder if it doesn't exist
            dest_folder = Path(self.downloads_path) / category
            dest_folder.mkdir(exist_ok=True)

            # Move the file
            shutil.move(str(file), str(dest_folder / file.name))
            logging.info(f"File organized: {file.name} -> {category}")

        except Exception as e:
            logging.error(f"Error organizing {file_path}: {str(e)}")

def signal_handler(signum, frame):
    """Signal handler for clean program shutdown"""
    logging.info(f"Stop signal received: {signal.Signals(signum).name}")
    logging.info("Stopping downloads organizer...")
    observer.stop()
    sys.exit(0)

def main():
    # Save PID for process control
    pid = os.getpid()
    pid_file = "downloads_organizer.pid"
    
    with open(pid_file, "w") as f:
        f.write(str(pid))
    
    logging.info(f"Organizer started with PID: {pid}")
    
    # Register signal handlers for controlled shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    try:
        # Get user's downloads path
        downloads_path = str(Path.home() / "Downloads")
        
        # Create organizer and observer
        global observer  # Needed for signal_handler
        organizer = FileOrganizer(downloads_path)
        observer = Observer()
        observer.schedule(organizer, downloads_path, recursive=False)
        observer.start()

        logging.info("Downloads organizer started - Checking every 2 hours")

        while True:
            logging.info("Starting pending files check...")
            organizer.process_pending_files()
            logging.info("Check completed. Next check in 2 hours")
            time.sleep(7200)  # 2 hours = 7200 seconds

    except Exception as e:
        logging.error(f"Error in main program: {str(e)}")
    finally:
        # Final cleanup
        if os.path.exists(pid_file):
            os.remove(pid_file)
        observer.stop()
        observer.join()
        logging.info("Organizer stopped and cleaned up properly")

if __name__ == "__main__":
    main()