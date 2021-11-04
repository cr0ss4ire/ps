#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

try:
    import pocstrike
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from libs.pocstrike.cli import check_environment, module_path
from libs.pocstrike import set_paths
from libs.pocstrike.lib.core.interpreter import PocstrikeInterpreter
from libs.pocstrike.lib.core.option import init_options


def main():
    check_environment()
    set_paths(module_path())
    init_options()
    poc = PocstrikeInterpreter()
    poc.start()


if __name__ == '__main__':
    main()
