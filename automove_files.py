from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os
import json
import time

image_extensions = ('.png', '.jpg', '.jpeg', '.svg', '.tiff')
video_extensions = ('.mov', '.mp4', '.mkv', '.avi', '.webm', '.mpeg', '.mpg', '.mpe',
                    '.mp2' '.ogg', '.wmv', '.mpv', '.m4p', '.m4v', '.qt', '.flv', '.swf', '.avchd')
installer_extensions = ('.exe', '.msi', '.dmg', '.pkg', '.deb')
audio_extensions = ('.mp3', '.m4a', '.wav', '.aiff',
                    '.acc', '.ogg', '.wma', '.flac', '.alac')
pdfs_extensions = ('.pdf')

folder_to_track = '/Users/sergi/Downloads'
generic_folder_destination = '/Users/sergi/Documents/other'
images_folder_destination = '/Users/sergi/Pictures'
videos_folder_destination = '/Users/sergi/Movies'
audios_folder_destination = '/Users/sergi/Music'
installers_folder_destination = '/Users/sergi/Documents/installers'
pdfs_folder_destination = '/Users/sergi/Documents/pdfs'


def destination(filename):
    extension = os.path.splitext(filename)[1]
    file_destination = {
        image_extensions: images_folder_destination + '/' + filename,
        video_extensions: videos_folder_destination + '/' + filename,
        audio_extensions: audios_folder_destination + '/' + filename,
        installer_extensions: installers_folder_destination + '/' + filename,
        pdfs_extensions: pdfs_folder_destination + '/' + filename
    }
    return file_destination.get(extension, generic_folder_destination + '/' + filename)


def move_files():
    for filename in os.listdir(folder_to_track):
        src = folder_to_track + '/' + filename
        new_destination = destination(filename)
        os.rename(src, new_destination)


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        move_files()


event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()
move_files()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
