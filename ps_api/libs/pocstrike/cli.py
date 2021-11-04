import os
import sys
import threading
import time
import traceback

try:
    import pocstrike
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir+'/'+os.path.pardir)))

from libs.pocstrike.lib.core.option import init
from libs.pocstrike.lib.core.option import init_options
from libs.pocstrike.lib.core.exception import PocstrikeUserQuitException, PocstrikeSystemException
from libs.pocstrike.lib.core.exception import PocstrikeShellQuitException
from libs.pocstrike.lib.core.common import set_paths
from libs.pocstrike.lib.core.common import banner
from libs.pocstrike.lib.core.common import data_to_stdout
from libs.pocstrike.lib.core.data import logger
from libs.pocstrike.lib.parse.cmd import cmd_line_parser
from libs.pocstrike.lib.controller.controller import start


def module_path():
    """
    This will get us the program's directory
    """
    return os.path.dirname(os.path.realpath(__file__))


def check_environment():
    try:
        os.path.isdir(module_path())
    except Exception:
        err_msg = "your system does not properly handle non-ASCII paths. "
        err_msg += "Please move the pocstrike's directory to the other location"
        logger.critical(err_msg)
        raise SystemExit


def main():
    """
    @function Main function of pocstrike when running from command line.
    """
    try:
        check_environment()
        set_paths(module_path())
        banner()
        init_options(cmd_line_parser().__dict__)

        data_to_stdout("[*] starting at {0}\n\n".format(time.strftime("%X")))
        init()
        try:
            start()
        except threading.ThreadError:
            raise

    except PocstrikeUserQuitException:
        pass

    except PocstrikeShellQuitException:
        pass

    except PocstrikeSystemException:
        pass

    except KeyboardInterrupt:
        pass

    except EOFError:
        pass

    except SystemExit:
        pass

    except Exception:
        exc_msg = traceback.format_exc()
        data_to_stdout(exc_msg)
        raise SystemExit

    finally:
        data_to_stdout("\n[*] shutting down at {0}\n\n".format(time.strftime("%X")))


if __name__ == "__main__":
    main()
