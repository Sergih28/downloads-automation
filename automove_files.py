from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

import os
import time

image_extensions = ('.png', '.jpg', '.jpeg', '.svg', '.tiff')
video_extensions = ('.mov', '.mp4', '.mkv', '.avi', '.webm', '.mpeg', '.mpg', '.mpe',
                    '.mp2', '.ogg', '.wmv', '.mpv', '.m4p', '.m4v', '.qt', '.flv', '.swf', '.avchd')
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
log_file = '/Users/sergi/Documents/startup/downloads_automation_log.txt'


def date_time():
    now = datetime.now()
    return now.strftime('%d/%m/%Y %H:%M:%S')


def print_to_log(message):
    f = open(log_file, 'a+')
    f.write(message + '\n')
    f.close()


def destination(filename):
    extension = os.path.splitext(filename)[1]
    if extension == '.download':
        return ''

    destination_folder = generic_folder_destination

    if extension in image_extensions:
        destination_folder = images_folder_destination
    elif extension in video_extensions:
        destination_folder = videos_folder_destination
    elif extension in audio_extensions:
        destination_folder = audios_folder_destination
    elif extension in installer_extensions:
        destination_folder = installers_folder_destination
    elif extension in pdfs_extensions:
        destination_folder = pdfs_folder_destination

    return destination_folder + '/' + filename


def move_files():
    for filename in os.listdir(folder_to_track):
        src = folder_to_track + '/' + filename
        new_destination = destination(filename)
        if new_destination != '':
            print_to_log(date_time() + ' Moving ' +
                         src + ' to ' + new_destination)
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
        time.sleep(3)
except KeyboardInterrupt:
    observer.stop()
observer.join()
