import os
import re
import subprocess

import cairocffi

from libqtile import bar
from libqtile.widget import base
from libqtile.widget.volume import Volume as _Volume
from libqtile.log_utils import logger

class VolumeIcon(_Volume):
    """
    Widget that displays an icon related to 
    the volume level
    """

    def __init__(self, **config):
        _Volume.__init__(self, **config)
        self.add_defaults(_Volume.defaults)
        self.volume = None

        if self.theme_path:
            self.length_type = bar.STATIC
            self.length = 0
        self.surfaces = {}
        self.current_icon = 'volume_off'
        self.icons = dict([(x, '{0}.png'.format(x)) for x in (
            'volume_down',
            'volume_up',
            'volume_off',
            'volume_mute',
            )])

    def _configure(self, qtile, bar):
        logger.error('Here I am')
        base._TextBox._configure(self, qtile, bar)
        self.setup_images()

    def _get_icon_key(self):
        key = 'volume'
        if self.volume == -1:
            key += '_off'
        elif self.volume <= 30:
            key += '_mute'
        elif self.volume <= 60:
            key += '_down'
        else:
            key += '_up'

        return key

    def timer_setup(self):
        self.timeout_add(self.update_interval, self.update)
        if self.theme_path:
            self.setup_images()

    def update(self):
        vol = self.get_volume()
        if vol != self.volume:
            self.volume = vol
            icon = self._get_icon_key()
            self.current_icon = icon
            self.draw()

        self.timeout_add(self.update_interval, self.update)

    def setup_images(self):
        for key, name in self.icons.items():
            try:
                path = os.path.join(self.theme_path, name)
                img = cairocffi.ImageSurface.create_from_png(path)
            except (cairocffi.Error, FileNotFoundError):
                self.theme_path = None
                logger.warning('VolumeIcons wrong icons path')
                return
            input_width = img.get_width()
            input_height = img.get_height()

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

    def draw(self):
        self.drawer.clear(self.background or self.bar.background)
        self.drawer.ctx.set_source(self.surfaces[self.current_icon])
        self.drawer.ctx.paint()
        self.drawer.draw(offsetx=self.offset, width=self.length)

