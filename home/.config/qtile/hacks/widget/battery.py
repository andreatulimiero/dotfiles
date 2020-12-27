from __future__ import division

import cairocffi
import os
from libqtile import bar, pangocffi, utils
from libqtile.log_utils import logger
from libqtile.widget import base, Battery as _Battery, BatteryIcon as _BatteryIcon
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 


from .base import InotifyText

BAT_DIR = '/sys/class/power_supply'
CHARGED = 'Full'
CHARGING = 'Charging'
DISCHARGING = 'Discharging'
UNKNOWN = 'Unknown'

BATTERY_INFO_FILES = {
    'energy_now_file': ['energy_now', 'charge_now'],
    'energy_full_file': ['energy_full', 'charge_full'],
    'power_now_file': ['power_now', 'current_now'],
    'status_file': ['status'],
}

def default_icon_path():
    # default icons are in libqtile/resources/battery-icons
    root = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2])
    return os.path.join(root, 'resources', 'battery-icons')


class IBattery(InotifyText):
    """Base battery class"""

    class BatteryChangeHandler(FileSystemEventHandler):

        def __init__(self, battery):
            super().__init__()
            self.battery = battery 

        def on_modified(self, event):
            # TODO: Check that modified file is actually the one we are inspecting
            # altought the worst case scenario is that we reload too much
            logger.error("Battery changed")
            #  self.battery.update()

    filenames = {}

    defaults = [
        ('battery_name', 'BAT1', 'ACPI name of a battery, usually BAT0'),
        (
            'status_file',
            'status',
            'Name of status file in'
            ' /sys/class/power_supply/battery_name'
        ),
        (
            'energy_now_file',
            None,
            'Name of file with the '
            'current energy in /sys/class/power_supply/battery_name'
        ),
        (
            'energy_full_file',
            None,
            'Name of file with the maximum'
            ' energy in /sys/class/power_supply/battery_name'
        ),
        (
            'power_now_file',
            None,
            'Name of file with the current'
            ' power draw in /sys/class/power_supply/battery_name'
        ),
        ('update_delay', 60, 'The delay in seconds between updates'),
    ]

    def __init__(self, **config):
        InotifyText.__init__(self, **config)
        self.add_defaults(_Battery.defaults)

    def _load_file(self, name):
        try:
            path = os.path.join(BAT_DIR, self.battery_name, name)
            with open(path, 'r') as f:
                return f.read().strip()
        except IOError:
            if name == 'current_now':
                return 0
            return False
        except Exception:
            logger.exception("Failed to get %s" % name)

    def _get_param(self, name):
        if name in self.filenames and self.filenames[name]:
            return self._load_file(self.filenames[name])
        elif name not in self.filenames:
            # Don't have the file name cached, figure it out

            # Don't modify the global list! Copy with [:]
            file_list = BATTERY_INFO_FILES.get(name, [])[:]

            if getattr(self, name, None):
                # If a file is manually specified, check it first
                file_list.insert(0, getattr(self, name))

            # Iterate over the possibilities, and return the first valid value
            for file in file_list:
                value = self._load_file(file)
                if value is not False and value is not None:
                    self.filenames[name] = file
                    return value

        # If we made it this far, we don't have a valid file.
        # Set it to None to avoid trying the next time.
        self.filenames[name] = None

        return None

    def _get_info(self):
        try:
            info = {
                'stat': self._get_param('status_file'),
                'now': float(self._get_param('energy_now_file')),
                'full': float(self._get_param('energy_full_file')),
                'power': float(self._get_param('power_now_file')),
            }
        except TypeError:
            return False
        return info


class Battery(_Battery):

    def _get_text(self):
        info = self._get_info()
        if info is False:
            return self.error_message

        return '{:.0%}'.format(info['now'] / info['full'])

class BatteryIcon(_BatteryIcon):

    def __init__(self, **config):
        _Battery.__init__(self, **config)
        self.add_defaults(BatteryIcon.defaults)

        if self.theme_path:
            self.length_type = bar.STATIC
            self.length = 0
        self.surfaces = {}
        self.current_icon = 'battery_full'
        self.icons = dict([(x, '{0}.png'.format(x)) for x in (
            'battery_20',
            'battery_30',
            'battery_50',
            'battery_60',
            'battery_80',
            'battery_90',
            'battery_charging_20',
            'battery_charging_30',
            'battery_charging_50',
            'battery_charging_60',
            'battery_charging_80',
            'battery_charging_90',
            'battery_charging_full',
            'battery_full'
            )])
        self.icons.update(self.custom_icons)


    def _get_icon_key(self):
        key = 'battery'
        info = self._get_info()
        if info is False or not info.get('full'):
            key += '-missing'
        else:
            if info['stat'] == CHARGING:
                key += '_charging'
            elif info['stat'] == CHARGED:
                key += '_full'
                return key

            percent = info['now'] / info['full']
            if percent <= .2:
                key += '_20'
            elif percent <= .3:
                key += '_30'
            elif percent <= .5:
                key += '_50'
            elif percent <= .6:
                key += '_60'
            elif percent <= .8:
                key += '_80'
            elif percent <= .9:
                key += '_90'
            else:
                key += '_full'

        return key

    def draw(self):
        self.drawer.clear(self.background or self.bar.background)
        self.drawer.ctx.set_source(self.surfaces[self.current_icon])
        self.drawer.ctx.paint()
        self.drawer.draw(offsetx=self.offset, width=self.length)

        #  self.drawer.set_source_rgb((0, 255, 0))
        #  self.drawer.ctx.rectangle(0, 20, 10, 10)
        #  self.drawer.ctx.fill()
        #  self.drawer.ctx.stroke()
        #  self.drawer.draw(offsetx=self.offset, width=self.length)

        #  layout = self.drawer.ctx.create_layout()
        #  layout.set_alignment(pangocffi.ALIGN_CENTER)
        #  layout.set_ellipsize(pangocffi.ELLIPSIZE_END)
        #  desc = pangocffi.FontDescription.from_string('Arial')
        #  desc.set_absolute_size(pangocffi.units_from_double(float(30)))
        #  layout.set_font_description(desc)
        #  layout.set_text(utils.scrub_to_utf8('$$$'))
        #  self.drawer.ctx.set_source_rgb(0, 255, 0)
        #  self.drawer.ctx.show_layout(layout)
        #  self.drawer.draw(offsetx=self.offset, width=self.length)

    def setup_images(self):
        for key, name in self.icons.items():
            try:
                path = os.path.join(self.theme_path, name)
                img = cairocffi.ImageSurface.create_from_png(path)
            except (cairocffi.Error, FileNotFoundError):
                self.theme_path = None
                logger.warning('Battery Icon switching to text mode')
                return
            input_width = img.get_width()
            input_height = img.get_height()

            #  sp = input_height / (self.bar.height - self.actual_padding)
            size = self.fontsize
            sp = input_height / size

            width = input_width / sp
            if width > self.length:
                # cast to `int` only after handling all potentially-float values
                self.length = int(width + self.actual_padding * 2)

            imgpat = cairocffi.SurfacePattern(img)

            scaler = cairocffi.Matrix()
            scaler.scale(sp, sp)

            translate_y = (self.bar.height - size) // 2
            scaler.translate(self.actual_padding * -1, -translate_y)

            imgpat.set_matrix(scaler)

            imgpat.set_filter(cairocffi.FILTER_BEST)
            self.surfaces[key] = imgpat

