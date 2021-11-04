import sys
import time
import os
from platform import system, machine

from libs.pocstrike import __version__
from libs.pocstrike.lib.core.revision import get_revision_number

VERSION = __version__
REVISION = get_revision_number()
SITE = ""
VERSION_STRING = "pocstrike/%s%s" % (VERSION, "-%s" % REVISION if REVISION else "-nongit-%s" % time.strftime("%Y%m%d",
                                                                                                            time.gmtime(
                                                                                                                os.path.getctime(
                                                                                                                    __file__.replace(
                                                                                                                        '.pyc',
                                                                                                                        '.py') if __file__.endswith(
                                                                                                                        'pyc') else __file__))))

IS_WIN = True if (sys.platform in ["win32", "cygwin"] or os.name == "nt") else False
PLATFORM = os.name
PYVERSION = sys.version.split()[0]

ISSUES_PAGE = ""
GIT_REPOSITORY = ""
GIT_PAGE = ""
ZIPBALL_PAGE = ""

LEGAL_DISCLAIMER = ""

BANNER = """
                               __         .__ __           
______   ____   ____   _______/  |________|__|  | __ ____  
\____ \ /  _ \_/ ___\ /  ___/\   __\_  __ \  |  |/ // __ \ 
|  |_> >  <_> )  \___ \___ \  |  |  |  | \/  |    <\  ___/ 
|   __/ \____/ \___  >____  > |__|  |__|  |__|__|_ \\___  >
|__|               \/     \/                      \/    \/

"""

# Encoding used for Unicode data
UNICODE_ENCODING = "utf-8"

DEFAULT_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"

BOLD_PATTERNS = ("' is vulnerable", "success", "\d    ",)

OLD_VERSION_CHARACTER = ("from comm import cmdline", "from comm import generic")
POCSTRIKE_VERSION_CHARACTER = ("from libs.pocstrike.poc import", "from libs.pocstrike.net import")
POC_IMPORTDICT = {
    "import urlparse": "from urllib import parse as urlparse",
    "import urllib2": "from urllib import request as urllib2",
    "import urllib": "from urllib import parse as urllib",
    "from urlparse import": "from urllib.parse import",
    "from libs.pocstrike.net import req": "from libs.pocstrike.lib.request import requests as req",
    "from libs.pocstrike.api.request import req": "from libs.pocstrike.lib.request import requests as req",
    "from libs.pocstrike.poc import": "from libs.pocstrike.lib.core.poc import",
    "from libs.pocstrike.api.poc import": "from libs.pocstrike.lib.core.poc import",
    "from libs.pocstrike.utils import register": "from libs.pocstrike.lib.core.register import register_poc as register",
    "from libs.pocstrike.lib.utils.funs import randomStr": "from libs.pocstrike.lib.utils import random_str as randomStr",
    "from libs.pocstrike.api.utils import randomStr": "from libs.pocstrike.lib.utils import random_str as randomStr",
    "from libs.pocstrike.lib.utils.funs import url2ip": "from libs.pocstrike.lib.utils import url2ip",
    "from libs.pocstrike.api.utils import url2ip": "from libs.pocstrike.lib.utils import url2ip",
    ".content": ".text",
}
# Regular expression used for recognition of IP addresses
IP_ADDRESS_REGEX = r"\b(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\b"
IP_ADDRESS_WITH_PORT_REGEX = r"\b(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[\d]{2,5}\b"
IPV6_ADDRESS_REGEX = r"^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$"
IPV6_URL_REGEX = r"(https?:\/\/)?\[((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\](:\d+)?(\/)?"
URL_ADDRESS_REGEX = r"(?:(?:https?):\/\/|www\.|ftp\.)(?:\([-a-zA-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-a-zA-Z0-9+&@#\/%=~_|$?!:,.])*(?:\([-a-zA-Z0-9+&@#\/%=~_|$?!:,.]*\)|[a-zA-Z0-9+&@#\/%=~_|$])"
URL_DOMAIN_REGEX = r"(?:www)?(?:[\w-]{2,255}(?:\.\w{2,6}){1,3})(?:/[\w&%?#-]{1,300})?(?:\:\d+)?"
LOCAL_IP_ADDRESS_REGEX = r"(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^192\.168\.)"

POC_REQUIRES_REGEX = r"install_requires\s*=\s*\[(?P<result>.*?)\]"

POC_NAME_REGEX = r'''(?sm)POCBase\):.*?name\s*=\s*['"](?P<result>.*?)['"]'''

MAX_NUMBER_OF_THREADS = 20

DEFAULT_LISTENER_PORT = 6666

# Maximum number of lines to save in history file
MAX_HISTORY_LENGTH = 1000

IMG_EXT = ('.jpg', '.png', '.gif')

TIMESTAMP = time.strftime('%Y%m%d%H%M%S', time.gmtime())
OS_SYSTEM = system().upper()
OS_ARCH = machine()

# Cmd line parse whitelist
CMD_PARSE_WHITELIST = ['url', 'url_file', 'verify', 'attack', 'shell', 'cookie', 'host', 'referer', 'configFile',
                       'agent', 'random_agent', 'proxy', 'proxy_cred', 'timeout', 'retry', 'delay', 'headers',
                       'max-page', 
                       'lhost', 'lport', 'plugins', 'pocs_path', 'threads', 'batch', 'check_requires', 'quiet', 'poc',
                       'verbose', 'mode', 'api', 'connect_back_host', 'connect_back_port', 'ppt', 'help']
