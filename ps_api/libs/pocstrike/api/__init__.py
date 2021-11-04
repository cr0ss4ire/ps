from libs.pocstrike.lib.controller.controller import start
from libs.pocstrike.lib.core.common import single_time_warn_message, encoder_bash_payload, encoder_powershell_payload, \
    get_host_ipv6
from libs.pocstrike.lib.core.data import conf, kb, logger, paths
from libs.pocstrike.lib.core.datatype import AttribDict
from libs.pocstrike.lib.core.enums import PLUGIN_TYPE, POC_CATEGORY, VUL_TYPE
from libs.pocstrike.lib.core.option import init, init_options
from libs.pocstrike.lib.core.plugin import PluginBase, register_plugin
from libs.pocstrike.lib.core.poc import POCBase, Output
from libs.pocstrike.lib.core.register import (
    load_file_to_module,
    load_string_to_module,
    register_poc,
)
from libs.pocstrike.lib.core.settings import DEFAULT_LISTENER_PORT
from libs.pocstrike.lib.request import requests
from libs.pocstrike.lib.utils import get_middle_text, generate_shellcode_list, random_str
from libs.pocstrike.modules.listener import REVERSE_PAYLOAD
from libs.pocstrike.modules.httpserver import PHTTPServer
from libs.pocstrike.shellcodes import OSShellcodes, WebShell
from libs.pocstrike.lib.core.interpreter_option import OptDict, OptIP, OptPort, OptBool, OptInteger, OptFloat, OptString, \
    OptItems, OptDict

__all__ = (
    'requests', 'PluginBase', 'register_plugin',
    'PLUGIN_TYPE', 'POCBase', 'Output', 'AttribDict', 'POC_CATEGORY', 'VUL_TYPE',
    'register_poc', 'conf', 'kb', 'logger', 'paths', 'DEFAULT_LISTENER_PORT', 'load_file_to_module',
    'load_string_to_module', 'single_time_warn_message', 'PHTTPServer', 'REVERSE_PAYLOAD', 'get_listener_ip', 'get_listener_port',
    'get_results', 'init_pocstrike', 'start_pocstrike', 'get_poc_options', 'crawl',
    'OSShellcodes', 'WebShell', 'OptDict', 'OptIP', 'OptPort', 'OptBool', 'OptInteger', 'OptFloat', 'OptString',
    'OptItems', 'OptDict', 'get_middle_text', 'generate_shellcode_list', 'random_str', 'encoder_bash_payload',
    'encoder_powershell_payload', 'get_host_ipv6')


def get_listener_ip():
    return conf.connect_back_host


def get_listener_port():
    return conf.connect_back_port


def get_current_poc_obj():
    pass


def get_poc_options(poc_obj=None):
    poc_obj = poc_obj or kb.current_poc
    return poc_obj.get_options()


def get_results():
    return kb.results


def init_pocstrike(options={}):
    init_options(options)
    init()


def start_pocstrike():
    start()
