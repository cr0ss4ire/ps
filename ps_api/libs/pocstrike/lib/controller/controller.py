import copy
import time

from libs.pocstrike.lib.core.common import data_to_stdout, desensitization
from libs.pocstrike.lib.core.data import conf, cmd_line_options
from libs.pocstrike.lib.core.data import kb
from libs.pocstrike.lib.core.data import logger
from libs.pocstrike.lib.core.datatype import AttribDict
from libs.pocstrike.lib.core.exception import PocstrikeValidationException, PocstrikeSystemException
from libs.pocstrike.lib.core.poc import Output
from libs.pocstrike.lib.core.settings import CMD_PARSE_WHITELIST
from libs.pocstrike.lib.core.threads import run_threads
from libs.pocstrike.modules.listener import handle_listener_connection
from libs.pocstrike.modules.listener.reverse_tcp import handle_listener_connection_for_console
from libs.pocstrike.thirdparty.prettytable.prettytable import PrettyTable


def runtime_check():
    if not kb.registered_pocs:
        error_msg = "no PoC loaded, please check your PoC file"
        logger.error(error_msg)
        raise PocstrikeSystemException(error_msg)


def start():
    runtime_check()
    tasks_count = kb.task_queue.qsize()
    info_msg = "pocstrike got a total of {0} tasks".format(tasks_count)
    logger.info(info_msg)
    logger.debug("pocstrike will open {} threads".format(conf.threads))

    try:
        run_threads(conf.threads, task_run)
        logger.info("Scan completed,ready to print")
    finally:
        task_done()

    if conf.mode == "shell" and not conf.api:
        info_msg = "connect back ip: {0}    port: {1}".format(
            desensitization(conf.connect_back_host) if conf.ppt else conf.connect_back_host, conf.connect_back_port)
        logger.info(info_msg)
        info_msg = "watting for shell connect to pocstrike"
        logger.info(info_msg)
        if conf.console_mode:
            handle_listener_connection_for_console()
        else:
            handle_listener_connection()


def show_task_result():
    if conf.quiet:
        return

    if not kb.results:
        return

    if conf.mode == "shell":
        return

    fields = ["target-url", "poc-name", "poc-id", "component", "version", "status"]
    results_table = PrettyTable(fields)
    results_table.align["target-url"] = "l"
    results_table.padding_width = 1

    total_num, success_num = 0, 0
    for row in kb.results:
        data = [
            row.target,
            row.poc_name,
            row.vul_id,
            row.app_name,
            row.app_version,
            row.status,
        ]
        results_table.add_row(data)
        total_num += 1
        if row.status == 'success':
            success_num += 1

    data_to_stdout('\n{0}'.format(results_table.get_string(sortby="status", reversesort=True)))
    data_to_stdout("\nsuccess : {} / {}\n".format(success_num, total_num))


def task_run():
    while not kb.task_queue.empty() and kb.thread_continue:
        target, vul_id = kb.task_queue.get()
        # if not conf.console_mode:
        poc_module = copy.deepcopy(kb.registered_pocs[vul_id])
        poc_name = poc_module.name

        # for hide some infomations
        if conf.ppt:
            info_msg = "running poc:'{0}' target '{1}'".format(poc_name, desensitization(target))
        else:
            info_msg = "running poc:'{0}' target '{1}'".format(poc_name, target)

        logger.info(info_msg)

        # hand user define parameters
        if hasattr(poc_module, "_options"):
            for item in kb.cmd_line:
                value = cmd_line_options.get(item, "")
                if item in poc_module.options:
                    poc_module.set_option(item, value)
                    info_msg = "Parameter {0} => {1}".format(item, value)
                    logger.info(info_msg)
            # check must be option
            for opt, v in poc_module.options.items():
                # check conflict in whitelist
                if opt in CMD_PARSE_WHITELIST:
                    info_msg = "Poc:'{0}' You can't customize this variable '{1}' because it is already taken up by the pocstrike.".format(
                        poc_name, opt)
                    logger.error(info_msg)
                    raise SystemExit

                if v.require and v.value == "":
                    info_msg = "Poc:'{poc}' Option '{key}' must be set,please add parameters '--{key}'".format(
                        poc=poc_name, key=opt)
                    logger.error(info_msg)
                    raise SystemExit

        try:
            result = poc_module.execute(target, headers=conf.http_headers, mode=conf.mode, verbose=False)
        except PocstrikeValidationException as ex:
            info_msg = "Poc:'{}' PocstrikeValidationException:{}".format(poc_name, ex)
            logger.error(info_msg)
            result = None

        if not isinstance(result, Output) and not None:
            _result = Output(poc_module)
            if result:
                if isinstance(result, bool):
                    _result.success({})
                elif isinstance(result, str):
                    _result.success({"Info": result})
                elif isinstance(result, dict):
                    _result.success(result)
                else:
                    _result.success({"Info": repr(result)})
            else:
                _result.fail()

            result = _result

        if not result:
            continue

        if not conf.quiet:
            result.show_result()

        result_status = "success" if result.is_success() else "failed"

        output = AttribDict(result.to_dict())
        '''if conf.ppt:
            # hide some information
            target = desensitization(target)'''

        output.update({
            'target': target,
            'vul_id': vul_id,
            'poc_name': poc_name,
            'created': time.strftime("%Y-%m-%d %X", time.localtime()),
            'status': result_status
        })
        # result_plugins_handle(output)
        kb.results.append(output)

        # TODO
        # set task delay


def result_plugins_start():
    """
    run result plugins, such as html report
    :return:
    """
    for _, plugin in kb.plugins.results.items():
        plugin.start()


def result_plugins_handle(output):
    """
    run result plugins when execute poc
    :return:
    """
    for _, plugin in kb.plugins.results.items():
        plugin.handle(output)


def task_done():
    show_task_result()
    result_plugins_start()
