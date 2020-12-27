import os
from libqtile import bar
from libqtile.widget import base
from libqtile.widget.base import _TextBox
from libqtile.log_utils import logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 

from .base import InotifyText

BACKLIGHT_DIR = '/sys/class/backlight'

class Backlight(InotifyText):
    """A simple widget to show the current brightness of a monitor"""

    class BrightnessChangeHandler(FileSystemEventHandler):

        def __init__(self, backlight):
            super().__init__()
            self.backlight = backlight

        def on_modified(self, event):
            # TODO: Check that modified file is actually the one we are inspecting
            # altought the worst case scenario is that we reload too much
            b = self.backlight
            b.info['brightness'] = float(b._load_file(b.brightness_file))
            b.tick()

    orientations = base.ORIENTATION_HORIZONTAL

    filenames = {}

    defaults = [
        ('backlight_name', 'intel_backlight', 'name of a backlight device'),
        (
            'brightness_file',
            'brightness',
            'Name of file with the '
            'current brightness in /sys/class/backlight/backlight_name'
        ),
        (
            'max_brightness_file',
            'max_brightness',
            'Name of file with the '
            'maximum brightness in /sys/class/backlight/backlight_name'
        ),
        ('scroll_step', 10, 'Percent of backlight every scroll changed'),
        (
            'brightness_min', 
            10, 
            'Minimum percent of backlight that can be selected'
            'so to avoid that the user cannot see the screen anymore'
        ),
        ('format', '{percent: 2.0%}', 'Display format')
    ]

    def __init__(self, **config):
        InotifyText.__init__(self, **config)
        self.add_defaults(Backlight.defaults)

        self.info = self._get_info()
        self.event_handler = self.BrightnessChangeHandler(self)
        self.file_handlers = [
                (self.event_handler, os.path.join(BACKLIGHT_DIR, self.backlight_name))
                ]
        self.register_handlers(self.file_handlers)

    def _configure(self, qtile, bar):
        should_tick = self.configured
        InotifyText._configure(self, qtile, bar)

        # Update when we are being re-configured.
        self.tick()

    def poll(self):
        percent = self.info['brightness'] / self.info['max']
        return self.format.format(percent=percent)

    def _load_file(self, name):
        try:
            path = os.path.join(BACKLIGHT_DIR, self.backlight_name, name)
            with open(path, 'r') as f:
                return f.read().strip()
        except:
            logger.exception("Failed to read file: %s" % name)
            raise

    def _get_info(self):
        try:
            info = {
                'brightness': float(self._load_file(self.brightness_file)),
                'max': float(self._load_file(self.max_brightness_file)),
            }
        except:
            return
        return info

    def change_backlight(self, value):
        """
        Change the backlight of the the scren by invoking an external command
        Note: We update the displayed value ourselves to make the widget more responsive
        Although it is true that it updates the widget twice, but thanks to the
        overall saving by not using polling this should make sense
        """
        self.info['brightness'] = self.info['max'] * value / 100
        self.tick()
        # FIXME: Calling this a lot of times in a short amount of time
        # (like scrolling up/down quickly) makes the whole WM crashing
        # This behaviour, happens only when calling such a program
        # (e.g. this does not happen by calling a dummy ['echo', 'hello world!']
        self.call_process(["light", "-S", str(value)])


    def step_brightness(self):
        value = self.info['brightness'] / self.info['max'] * 100
        if value < 25:
            self.change_backlight(25)
        elif value < 50:
            self.change_backlight(50)
        elif value < 75:
            self.change_backlight(75)
        elif value < 100:
            self.change_backlight(100)
        else:
            self.change_backlight(25)

    def button_press(self, x, y, button):
        if button == 1: # Simple click/tap
            self.step_brightness()
        else:
            value = self.info['brightness'] / self.info['max'] * 100
            if button == 4:  # up
                self.change_backlight(max(value - self.scroll_step, self.brightness_min))
            elif button == 5: # down 
                self.change_backlight(min(value + self.scroll_step, 100))

