import sys
import logging

from libs.pocstrike.lib.core.enums import CUSTOM_LOGGING

logging.addLevelName(CUSTOM_LOGGING.SYSINFO, "*")
logging.addLevelName(CUSTOM_LOGGING.SUCCESS, "+")
logging.addLevelName(CUSTOM_LOGGING.ERROR, "-")
logging.addLevelName(CUSTOM_LOGGING.WARNING, "!")

LOGGER = logging.getLogger("pocstrike")

LOGGER_HANDLER = None
LOGGER_FILE_HANDLER = None
try:
    from libs.pocstrike.thirdparty.ansistrm.ansistrm import ColorizingStreamHandler

    disableColor = False

    for argument in sys.argv:
        if "disable-col" in argument:
            disableColor = True
            break

    if disableColor:
        LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
        LOGGER_FILE_HANDLER = logging.FileHandler("pocstrike.log")
    else:
        LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
        LOGGER_HANDLER.level_map[logging.getLevelName("*")] = (None, "cyan", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("+")] = (None, "green", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("-")] = (None, "red", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("!")] = (None, "yellow", False)
        LOGGER_FILE_HANDLER = logging.FileHandler("pocstrike.log", encoding='utf-8')
except ImportError:
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
    LOGGER_FILE_HANDLER = logging.FileHandler("pocstrike.log")

FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")

LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER_FILE_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_FILE_HANDLER)
LOGGER.setLevel(logging.INFO)
