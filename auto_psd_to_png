import sys
import os
import time
from psd_tools import PSDImage
from watchdog.observers import Observer
import watchdog.events

print("#AUTOMATIC PHOTOSHOP TO PNG ACTIVATED!")

class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self, *args, **kwargs):
        watchdog.events.PatternMatchingEventHandler.__init__(
            self, patterns=['*.psd'], ignore_directories=True, case_sensitive=False
        )

    def on_moved(self, event):
        if (event):
            try:
                print("TRYING TO OPEN PSD FILE: " + event.dest_path)
                psd = PSDImage.open(event.dest_path)
                print("SUCESSFULLY OPENED PSD FILE")
                new_path = event.dest_path.replace(".psd", ".png")
                print("SAVING PNG FILE: " + new_path)
                psd.compose().save(new_path)
                print("FINISHED CONVERTING PSD -> PNG")
            except: 
                print("[!] Something went wrong~!")

    def on_modified(self, event):
        pass #when you saved the psd file first time.
        
if __name__ == "__main__":
    file_handler = Handler()
    observer = Observer()
    observer.schedule(file_handler, '.', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
