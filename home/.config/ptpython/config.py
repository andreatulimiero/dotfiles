from __future__ import unicode_literals
from prompt_toolkit.filters import ViInsertMode
from prompt_toolkit.key_binding.key_processor import KeyPress
from prompt_toolkit.keys import Keys
from pygments.token import Token

from ptpython.layout import CompletionVisualisation

__all__ = (
    'configure',
)


def configure(repl):
    # Vi mode.
    repl.vi_mode = True
    # Show function signature (bool).
    repl.show_signature = True
    # Highlight matching parethesis.
    repl.highlight_matching_parenthesis = True
    # Colorscheme
    repl.use_code_colorscheme('monokai')

    @repl.add_key_binding('k', 'j', filter=ViInsertMode())
    def _(event):
        " Map 'kj' to Escape. "
        event.cli.key_processor.feed(KeyPress(Keys.Escape))

    @repl.add_key_binding('j', 'k', filter=ViInsertMode())
    def _(event):
        " Map 'kj' to Escape. "
        event.cli.key_processor.feed(KeyPress(Keys.Escape))
