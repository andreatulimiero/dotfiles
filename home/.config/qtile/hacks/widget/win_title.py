from libqtile import hook, bar
from libqtile.widget import base


class WindowName(base._TextBox):
    """Displays the name of the window that currently has focus"""
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ('show_state', True, 'show window status before window name'),
        ('for_current_screen', False, 'instead of this bars screen use currently active screen'),
        ('max_length', 30, 'maximum number of characters to show for the state')
    ]

    def __init__(self, width=bar.STRETCH, **config):
        base._TextBox.__init__(self, width=width, **config)
        self.add_defaults(WindowName.defaults)

    def _configure(self, qtile, bar):
        base._TextBox._configure(self, qtile, bar)
        hook.subscribe.window_name_change(self.update)
        hook.subscribe.focus_change(self.update)
        hook.subscribe.float_change(self.update)

        @hook.subscribe.current_screen_change
        def on_screen_changed():
            if self.for_current_screen:
                self.update()

    def update(self):
        if self.for_current_screen:
            w = self.qtile.currentScreen.group.currentWindow
        else:
            w = self.bar.screen.group.currentWindow
        state = ''
        if self.show_state and w is not None:
            if w.maximized:
                state = '[] '
            elif w.minimized:
                state = '_ '
            elif w.floating:
                state = 'V '
        self.text = "%s%s" % (state, w.name if w and w.name else " ")
        if len(self.text) > self.max_length:
            self.text = self.text[:self.max_length//2] + "…" + self.text[-self.max_length//2:]
        self.bar.draw()

