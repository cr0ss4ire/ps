from flask import Blueprint, request, g
import os
import threading
import time
import traceback
import time
from apps.exploit.models import Exploit, VulType, Category, Application, Level, Language, Effect
from apps.account.models import User
from apps.task.models import Task, ExecModel
# from apps.configuration.models import ConfigKey, AppConfigRel, Environment
# from apps.assets.models import Host
from libs.tools import json_response, JsonParser, Argument, AttrDict
# from libs.utils import Container
# from docker.errors import DockerException
from datetime import datetime
from public import executor
from libs.decorators import require_permission
from libs.pocstrike.lib.core.option import init
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
# from apps.deploy.utils import get_built_in_menus

blueprint = Blueprint(__name__, __name__)


@blueprint.route('/exec_models', methods=['GET'])
@require_permission('task_view')
def search_levels():
    query = ExecModel.query
    exec_models = query.all()
    total = query.count()
    return json_response({'data': [x.to_json() for x in exec_models], 'total': total})


def task_exec(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        task.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task.status = 1
        task.save()
        banner()
        options = {
            'verbose': 2,
            'url': ['http://192.168.2.245', 'http://192.168.2.245:8080'],
            'url_file': None,
            'poc': ['_2_drupal_rce.py', '_1_tomcat_upload.py'],
            'configFile': None,
            'mode': 'attack',
            'cookie': None,
            'host': None,
            'referer': None,
            'agent': None,
            'random_agent': False,
            'proxy': None,
            'proxy_cred': None,
            'timeout': None,
            'retry': False,
            'delay': None,
            'headers': None,
            'connect_back_host': None,
            'connect_back_port': None,
            'plugins': None,
            'pocs_path': None,
            'threads': 1,
            'batch': None,
            'check_requires': False,
            'quiet': False,
            'ppt': False
        }
        init_options(options)
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


@blueprint.route('/start/<int:task_id>', methods=['GET'])
@require_permission('task_view')
def start_task(task_id):
    executor.submit(task_exec, task_id)
    return json_response()


@blueprint.route('/edit/<int:task_id>', methods=['GET'])
@require_permission('task_view')
def get_task(task_id):
    query = Task.query.filter(Task.id == task_id)
    return json_response(data=query.first())


@blueprint.route('/index', methods=['GET'])
@require_permission('task_view')
def get():
    form, error = JsonParser(
        Argument('page', type=int, default=1, required=False),
        Argument('pagesize', type=int, default=10, required=False),
        Argument('task_query', type=dict, default={}),
    ).parse(request.args)
    if error is None:
        query = Task.query.join(User, User.id == Task.user_id).with_entities(
            Task.id, Task.name, Task.status, Task.create_time, Task.update_time, Task.start_time, Task.finish_time,
            User.nickname)

        if form.page == -1:
            return json_response(message="页面不能小于0")
        if form.task_query.get('name'):
            query = query.filter(
                Task.name.like('%{}%'.format(form.task_query['name'])))

        if form.task_query.get('task_status'):
            query = query.filter(Task.status ==
                                 form.task_query.get('task_status'))
        query = query.filter(Task.user_id == g.user.id).order_by(Task.id.desc())

        result = query.limit(form.pagesize).offset(
            (form.page - 1) * form.pagesize).all()
        return json_response({
            'data': [dict(zip(['id', 'name', 'status', 'create_time', 'update_time', 'start_time', 'finish_time',
                               'author'], list(x))) for x in result],
            'total': query.count()
        })
    return json_response(message=error)


'''@blueprint.route('/vultypes', methods=['GET'])
@require_permission('exploit_view')
def search_vultypes():
    query = VulType.query
    vultypes = query.all()
    total = query.count()
    return json_response({'data': [x.to_json() for x in vultypes], 'total': total})





@blueprint.route('/effects', methods=['GET'])
@require_permission('exploit_view')
def search_effects():
    query = Effect.query
    effects = query.all()
    total = query.count()
    return json_response({'data': [x.to_json() for x in effects], 'total': total})


@blueprint.route('/applications', methods=['GET'])
@require_permission('exploit_view')
def search_applications():
    query = Application.query
    applications = query.all()
    total = query.count()
    return json_response({'data': [x.to_json() for x in applications], 'total': total})


@blueprint.route('/categories', methods=['GET'])
@require_permission('exploit_view')
def search_categories():
    query = Category.query
    categories = query.all()
    total = query.count()
    return json_response({'data': [x.to_json() for x in categories], 'total': total})


@blueprint.route('/languages', methods=['GET'])
@require_permission('exploit_view')
def search_languages():
    query = Language.query
    languages = query.all()
    total = query.count()
    return json_response({'data': [x.to_json() for x in languages], 'total': total})'''


@blueprint.route('/file_upload', methods=['POST'])
@require_permission('task_view')
def file_upload():
    file = request.files['url_file']
    if file.filename.rsplit('.', 1)[1].lower() == "txt":
        try:
            alise_name = str(int(time.time()))+"_"+file.filename
            upload_path = "./upload/"+str(g.user.id)+"/task_targets/"
            if not os.path.exists(upload_path):
                os.mkdir(upload_path)
            file.save(os.path.join(upload_path, alise_name))
            return json_response({"status": "上传成功", "file_list": [{"name": file.filename, "path": os.path.join(upload_path, alise_name)}]})
        except Exception:
            return json_response(message="上传失败")
    else:
        return json_response(message="只能上传txt文件")


@blueprint.route('/add', methods=['POST'])
@require_permission('task_add')
def add():
    args = AttrDict(name=Argument('name', type=str, help='请输入任务名称!'),
                    url_list=Argument('url_list', type=str, default="", help='请输入目标列表!'),
                    plugins=Argument(
                        'plugins', type=str, help='请选择漏洞插件!'),
                    desc=Argument('desc', type=str, help='请输入任务描述!'),
                    url_file_path=Argument('url_file_path', type=str, default="", help='请选择目标文件!'),
                    exec_model_id=Argument(
                        'exec_model_id', type=int, help='请选择攻击模式！'))
    form, error = JsonParser(*args.values()).parse()
    if error is None:
        if Task.query.filter(Task.name == form.name).first():
            return json_response(message='任务名称不能重复！')
        task = Task(**form)
        task.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task.update_time = ""
        task.user_id = g.user.id
        task.start_time = ""
        task.finish_time = ""
        task.status = 0
        task.save()
        return json_response(data=task)
    return json_response(message=error)


@blueprint.route('/plugins/<int:plugin_id>', methods=['DELETE'])
@require_permission('publish_app_del')
def delete(plugin_id):
    plugin = Exploit.query.get_or_404(plugin_id)
    plugin.delete()
    return json_response()


@blueprint.route('/edit/<int:task_id>', methods=['PUT'])
@require_permission('task_edit')
def put(task_id):
    args = AttrDict(name=Argument('name', type=str, help='请输入任务名称!'),
                    url_list=Argument('url_list', type=str, default="", help='请输入目标列表!'),
                    plugins=Argument(
                        'plugins', type=str, help='请选择漏洞!'),
                    desc=Argument('desc', type=str, help='请输入任务描述!'),
                    url_file_path=Argument('url_file_path', type=str, default="", help='请选择目标文件!'),
                    exec_model_id=Argument(
                        'exec_model_id', type=int, help='请选择任务执行模式！'))
    form, error = JsonParser(*args.values()).parse()
    if error is None:
        exists_record = Task.query.filter(Task.name == form.name).first()
        if exists_record and exists_record.id != task_id:
            return json_response(message='任务名称不能重复！')
        task = Task.query.get_or_404(task_id)
        task.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task.update(**form)
        task.save()
        return json_response(task)
    return json_response(message=error)
