import traceback
import importlib

from libqtile.log_utils import logger


def safe_import(module_name, class_name):
    """
    try to import a module, and if it fails because an ImporError
    it logs on WARNING, and logs the traceback on DEBUG level
    """
    if type(class_name) is list:
        for name in class_name:
            safe_import(module_name, name)
        return
    package = __package__
    # TODO: remove when we really want to drop 3.2 support
    # python 3.2 don't set __package__
    if not package:
        package = __name__
    try:
        module = importlib.import_module(module_name, package)
        globals()[class_name] = getattr(module, class_name)
    except ImportError as error:
        logger.warning("Unmet dependencies for optional Widget: '%s.%s', %s",
                       module_name, class_name, error)
        logger.debug("%s", traceback.format_exc())


safe_import(".battery", ["Battery", "BatteryIcon"])
safe_import(".backlight", ["Backlight"])
safe_import(".volume", ["VolumeIcon"])
safe_import(".win_title", ["WindowName"])
safe_import(".player", ["Player"])
