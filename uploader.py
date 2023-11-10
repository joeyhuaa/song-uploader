import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class MyHandler(FileSystemEventHandler):
    def __init__(self, drive, drive_folder_id):
        super().__init__()
        self.drive = drive
        self.drive_folder_id = drive_folder_id

    def on_created(self, event):
        if event.is_directory:
            return
        print(f"New file created: {event.src_path}")
        self.upload_to_drive(event.src_path)

    def upload_to_drive(self, file_path):
        file_name = file_path.split("/")[-1]
        drive_file = self.drive.CreateFile({'title': file_name, 'parents': [{'id': self.drive_folder_id}]})
        drive_file.Upload()
        print(f"File {file_name} uploaded to Google Drive.")

def authenticate_drive():
    gauth = GoogleAuth()
    # gauth.LocalWebserverAuth('clients_secrets.json', 6000, True)
    # gauth.LocalWebserverAuth()
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)
    return drive

def monitor_directory(path, drive_folder_id):
    drive = authenticate_drive()
    event_handler = MyHandler(drive, drive_folder_id)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    directory_to_monitor = "/Users/joeyhua/Desktop/Music/Songs"
    drive_folder_id = "16ddctXXekK2JCPGQZDx1xK7kxcj0HF0A" #change this
    monitor_directory(directory_to_monitor, drive_folder_id)

