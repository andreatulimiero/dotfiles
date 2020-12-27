import subprocess
from libqtile.log_utils import logger
from libqtile.widget.base import ThreadPoolText, ORIENTATION_HORIZONTAL

from . import base

ellipsize = lambda n, m: n if len(n) <= m else n[:m] + "…"

class Player(ThreadPoolText):
    """
    A simple player widget
    """
    orientations = ORIENTATION_HORIZONTAL
    defaults = [
        ('play_color', '00ff00', 'Text colour when playing.'),
        ('noplay_color', 'cecece', 'Text colour when not playing.'),
        ('max_artist_len', 10, 'Maximum number of characters to display for artist\'s name'),
        ('max_title_len', 15, 'Maximum number of characters to display for the title'),
        ('update_interval', 0.5, 'Update Time in seconds.')
    ]

    def __init__(self, **config):
        ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(Player.defaults)
        self.status = ""
        self.max_chars = self.max_artist_len + self.max_title_len

    def now_playing(self):
        """Return a string with the now playing info (Artist - Song Title)."""
        self.status = self.call_process(["playerctl", "status"]).strip()
        if self.status == "No players found":
            self.status = None
            return ""
        elif self.status == "Playing":
            self.layout.colour = self.play_color
        elif self.status == "Paused":
            self.layout.colour = self.noplay_color
        else:
            self.status = None
            return ""

        now_playing = ""
        try:
            artist = ellipsize(
                    self.call_process(["playerctl", "metadata", "artist"]).strip(),
                    self.max_artist_len)
            title = ellipsize(
                    self.call_process(["playerctl", "metadata", "title"]).strip(),
                    self.max_title_len)
            now_playing = artist + " - " + title
        except Exception as e:
            logger.error(str(e))

        return now_playing

    def update(self, text):
        """Update the text box."""
        old_width = self.layout.width
        if not self.status:
            return
        if len(text) > self.max_chars > 0:
            text = text[:self.max_chars] + "…"
        self.text = text

        if self.layout.width == old_width:
            self.draw()
        else:
            self.bar.draw()

    def poll(self):
        """Poll content for the text box."""
        return self.now_playing()

    def button_press(self, x, y, button):
        if button == 1: # Simple click/tap
            subprocess.Popen(['playerctl', 'play-pause'])
        elif button == 2: # 3-fingers tap/Middle button
            subprocess.Popen(['playerctl', 'prev'])
        elif button == 3: # 2-fingers tap/Right button
            subprocess.Popen(['playerctl', 'next'])

