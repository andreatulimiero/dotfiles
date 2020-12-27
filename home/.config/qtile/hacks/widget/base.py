from libqtile.log_utils import logger
from libqtile import command, bar, configurable, drawer, confreader
from libqtile.widget.base import _TextBox
import six
import subprocess
import threading
import warnings

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 

class InotifyText(_TextBox):
    """ 
    A common interface for text based widgets that watch for file
    changes and gets notified by the system with inotify
    """


    def __init__(self, **config):
        _TextBox.__init__(self, 'N/A', width=bar.CALCULATED, **config)
        #  self.add_defaults()

    def _configure(self, qtile, bar):
        should_tick = self.configured
        _TextBox._configure(self, qtile, bar)

        # Update when we are being re-configured.
        if should_tick:
            self.tick()

    def register_handlers(self, file_handlers:tuple):
        self.observer = Observer()
        for handler, file_path in file_handlers:
            self.observer.schedule(handler, path=file_path, recursive=False)
        self.observer.start()

    def poll(self):
        return 'N/A'

    def tick(self):
        text = self.poll()
        self.update(text)

    def update(self, text):
        old_width = self.layout.width
        self.text = text
        new_width = self.layout.width
        # If our width hasn't changed, we just draw ourselves. Otherwise,
        # we draw the whole bar.
        if new_width == old_width:
            self.draw()
        else:
            self.bar.draw()

