import argparse
import os
import sys

from libs.pocstrike.lib.core.common import data_to_stdout
from libs.pocstrike.lib.core.settings import IS_WIN, CMD_PARSE_WHITELIST

DIY_OPTIONS = []


def cmd_line_parser(argv=None):
    """
    This function parses the command line parameters and arguments
    """

    if not argv:
        argv = sys.argv

    _ = os.path.basename(argv[0])
    usage = "python cli.py [options]"
    parser = argparse.ArgumentParser(prog='pocstrike', usage=usage)
    try:

        parser.add_argument("-v", dest="verbose", type=int, default=2, choices=list(range(1, 7)),
                            help="Verbosity level: 1-6 (default 2)")

        # Target options
        target = parser.add_argument_group('Target', "At least one of these "
                                                     "options has to be provided to define the target(s)")
        target.add_argument("-u", "--url", dest="url", nargs='+',
                            help="Target URL (e.g. \"http://www.test.com/vuln.php?id=1\")")

        target.add_argument("-f", "--file", dest="url_file", help="Scan multiple targets given in a textual file")
        target.add_argument("-r", dest="poc", nargs='+', help="Load POC file from local")
        target.add_argument("-c", dest="configFile", help="Load options from a configuration INI file")

        # Mode options
        mode = parser.add_argument_group("Mode", "Pocstrike running mode options")

        mode.add_argument("--verify", dest="mode", default='verify', action="store_const", const='verify',
                          help="Run poc with verify mode")

        mode.add_argument("--attack", dest="mode", action="store_const", const='attack',
                          help="Run poc with attack mode")
        mode.add_argument("--shell", dest="mode", action="store_const", const='shell',
                          help="Run poc with shell mode")
        # Requests options
        request = parser.add_argument_group("Request", "Network request options")
        request.add_argument("--cookie", dest="cookie", help="HTTP Cookie header value")
        request.add_argument("--host", dest="host", help="HTTP Host header value")
        request.add_argument("--referer", dest="referer", help="HTTP Referer header value")
        request.add_argument("--user-agent", dest="agent", help="HTTP User-Agent header value")
        request.add_argument("--random-agent", dest="random_agent", action="store_true", default=False,
                             help="Use randomly selected HTTP User-Agent header value")
        request.add_argument("--proxy", dest="proxy", help="Use a proxy to connect to the target URL")
        request.add_argument("--proxy-cred", dest="proxy_cred", help="Proxy authentication credentials (name:password)")
        request.add_argument("--timeout", dest="timeout", help="Seconds to wait before timeout connection (default 30)")
        request.add_argument("--retry", dest="retry", default=False, help="Time out retrials times.")
        request.add_argument("--delay", dest="delay", help="Delay between two request of one thread")
        request.add_argument("--headers", dest="headers", help="Extra headers (e.g. \"key1: value1\\nkey2: value2\")")
              
        # Modules options
        modules = parser.add_argument_group("Modules", "Modules(Listener) options")
        
        modules.add_argument("--lhost", dest="connect_back_host", action="store", default=None,
                             help="Connect back host for target PoC in shell mode")
        modules.add_argument("--lport", dest="connect_back_port", action="store", default=None,
                             help="Connect back port for target PoC in shell mode")

        # Optimization options
        optimization = parser.add_argument_group("Optimization", "Optimization options")
        optimization.add_argument("--plugins", dest="plugins", action="store", default=None,
                                  help="Load plugins to execute")
        optimization.add_argument("--pocs-path", dest="pocs_path", action="store", default=None,
                                  help="User defined poc scripts path")
        optimization.add_argument("--threads", dest="threads", type=int, default=1,
                                  help="Max number of concurrent network requests (default 1)")
        optimization.add_argument("--batch", dest="batch",
                                  help="Automatically choose defaut choice without asking.")
        optimization.add_argument("--requires", dest="check_requires", action="store_true", default=False,
                                  help="Check install_requires")
        optimization.add_argument("--quiet", dest="quiet", action="store_true", default=False,
                                  help="Activate quiet mode, working without logger.")
        optimization.add_argument("--ppt", dest="ppt", action="store_true", default=False,
                                  help="Hiden sensitive information when published to the network")

        # Diy options
        diy = parser.add_argument_group("Poc options", "definition options for PoC")

        for line in argv:
            if line.startswith("--"):
                if line[2:] not in CMD_PARSE_WHITELIST:
                    diy.add_argument(line)

        args = parser.parse_args()
        if not any((args.url, args.url_file, args.plugins, args.configFile)):
            err_msg = "missing a mandatory option (-u, -f). "
            err_msg += "Use -h for basic and -hh for advanced help\n"
            parser.error(err_msg)

        return args

    except SystemExit:
        # Protection against Windows dummy double clicking
        if IS_WIN:
            data_to_stdout("\nPress Enter to continue...")
            input()
        raise
