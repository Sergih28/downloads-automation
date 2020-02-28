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


def get_file_name(path):
    return os.path.splitext(path)[0]


def get_file_extension(path):
    return os.path.splitext(path)[1]


def check_file_exists(path):
    return os.path.exists(path)


def check_file_completed(filename):
    historical_size = -1
    while (check_file_exists(filename) and historical_size != os.path.getsize(filename)):
        # print(str(historical_size) + ' - ' + str(os.path.getsize(filename)))
        historical_size = os.path.getsize(filename)
        time.sleep(1)
    # if check_file_exists(filename):
        # print(str(historical_size) + ' - ' + str(os.path.getsize(filename)))


def destination(path, filename):
    destination_folder = generic_folder_destination
    # print('isfile: ' + str(os.path.isfile(path)) + '  -- ' + filename)
    if os.path.isfile(path):
        extension = get_file_extension(filename)
        # print('extensione: ' + extension)
        if extension == '.download':
            check_file_completed(filename)
            return ''

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


def move_files(n, file_completed=False):
    for filename in os.listdir(folder_to_track):
        # omit .DS_Store files
        if get_file_name(filename) == '.DS_Store':
            continue

        src = folder_to_track + '/' + filename
        # check if it has finished copying / downloading it
        if not file_completed:
            check_file_completed(src)
        # print('file should be completed')
        # if file doens't exist anymore, start again
        if not check_file_exists(src):
            move_files(n, True)
            return

        if n > 1:
            filename = get_file_name(
                filename) + ' (' + str(n) + ')' + get_file_extension(filename)
        new_destination = destination(src, filename)
        # print('filename: ' + filename)

        if new_destination != '':
            if not check_file_exists(new_destination):
                print_to_log(date_time() + ' Moving ' +
                             src + ' to ' + new_destination)
                os.rename(src, new_destination)
            else:  # if file exists, retry with a new name
                move_files(n+1, True)
        else:
            move_files(n, False)


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        move_files(1)


event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()
move_files(1)

try:
    while True:
        time.sleep(3)
except KeyboardInterrupt:
    observer.stop()
observer.join()
