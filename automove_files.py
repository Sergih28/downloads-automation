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


def check_file_completed(path):
    historical_size = -1
    extension = get_file_extension(path)
    downloading_extensions = ('.crdownload', '.download', '.part', '.partial')

    if extension in downloading_extensions:
        print('Download extension detected:' + extension)
        time.sleep(2)
        print('Checking again if the extension has changed')
        return False

    while (historical_size != os.path.getsize(path)):
        if historical_size != -1:
            print(path + ' -- Waiting for the file to be complete')
        historical_size = os.path.getsize(path)
        time.sleep(2)

    print(path + ' -- File ready to be moved')
    return True


def get_new_destination(path, filename, destination):
    # check if the file already exists on the destination folder
    # If so, keep adding a number until it doesn't exist
    if not check_file_exists(destination):
        print('Destination: ' + destination)
        return destination

    counter = 1
    print('File exists on the destination folder, giving it a new name')
    while True:
        counter = counter + 1
        new_destination = get_file_name(
            destination) + ' (' + str(counter) + ')' + get_file_extension(destination)

        if not check_file_exists(new_destination):
            destination = new_destination
            print('New name: ' + destination)
            break
    return destination


def destination(path, filename):
    destination_folder = generic_folder_destination

    if os.path.isfile(path):
        extension = get_file_extension(filename)

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


def move_files():
    files = os.listdir(folder_to_track)
    # omit hidden files
    filtered_files = [x for x in files if not x.startswith('.')]

    for filename in filtered_files:
        src = folder_to_track + '/' + filename

        if not check_file_completed(src):
            move_files()
            break

        new_destination = destination(src, filename)
        new_destination = get_new_destination(src, filename, new_destination)

        print(date_time() + ' Moving ' +
              src + ' to ' + new_destination)
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
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
