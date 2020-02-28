# downloads-automation

## What it does

- Moves automatically downloaded files into different folders, depending on its extension.
  It excludes hidden files.
- Detects if a file hasn't completed downloading and waits until it has to move it.
- Creates a log with the timestamp, origin and destination of the file that is being moved.
- Outputs on the console some feedback about what steps it is doing.
- If used with _Cron_ as explained below, it outputs the errors as well, and it's always running in the background.
- _When referring to files, same things apply to folders._

## What I learned

- Basic stuff with Python (_function, class, tuple, loop_)
- File management with Python (writing a log)
- Refreshed my knowledge about _Cron_

## Requirements

- Python 3 (_version 3.8.1 used when creating the script_)
- Watchdog package (_pip install watchdog_)

## How to set up (macOS 10.15.3)

1. Clone the repository
1. Install Python 3
1. Install pip
1. Create a crontab file
   - _crontab /Users/sergi/Documents/crontab_
1. Add this line to crontab, that will execute automatically the script every time we boot up the OS and throw any errors in a file:

   - **_@reboot cd /Users/sergi/Documents/downloads-automation && ./downloads_automation.sh 2>/Users/sergi/Documents/startup/downloads_automation_error.txt_**

1. Restart, and enjoy!

App idea taken from [Kalle Hallden](https://github.com/KalleHallden) on his [video](https://www.youtube.com/watch?v=A3PRB1Wc0UA)
