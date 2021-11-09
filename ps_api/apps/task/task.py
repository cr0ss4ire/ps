from flask import Blueprint, request, g, url_for, send_from_directory
import os
import sys
import threading
import time
import traceback
import time
from apps.exploit.models import Exploit, VulType, Category, Application, Level, Language, Effect
from apps.account.models import User
# from apps.configuration.models import ConfigKey, AppConfigRel, Environment
# from apps.assets.models import Host
from libs.tools import json_response, JsonParser, Argument, AttrDict
# from libs.utils import Container
# from docker.errors import DockerException
from datetime import datetime
# from public import db
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


@blueprint.route('/start/<int:task_id>', methods=['GET'])
# @require_permission('exploit_view')
def start_task(task_id):
    try:
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
        data_to_stdout(
            "\n[*] shutting down at {0}\n\n".format(time.strftime("%X")))
    '''query = Exploit.query.join(
            Category, Category.id == Exploit.category_id).join(
                VulType, VulType.id == Exploit.vul_type_id).join(
                    Application,
                    Application.id == Exploit.application_id).join(
                        Level, Level.id == Exploit.vullevel_id).join(
                            Language, Language.id == Exploit.language_id).join(
                                Effect, Effect.id == Exploit.effect_id).join(
                                    User, User.id == Exploit.user_id).with_entities(
                                        Exploit.affect_version, Exploit.enter_time, Exploit.update_time, Language.name, Exploit.os,
                                        Exploit.desc).filter(Exploit.id == plugin_id)'''
    return json_response()


@blueprint.route('/task/<int:task_id>', methods=['GET'])
@require_permission('task_view')
def get_plugin(plugin_id):
    query = Exploit.query.filter(Exploit.id == plugin_id)
    return json_response(query.first())


@blueprint.route('/index', methods=['GET'])
@require_permission('task_view')
def get():
    form, error = JsonParser(
        Argument('page', type=int, default=1, required=False),
        Argument('pagesize', type=int, default=10, required=False),
        Argument('plugin_query', type=dict, default={}),
    ).parse(request.args)
    if error is None:
        query = Exploit.query.join(
            Category, Category.id == Exploit.category_id).join(
                VulType, VulType.id == Exploit.vul_type_id).join(
                    Application,
                    Application.id == Exploit.application_id).join(
                        Level, Level.id == Exploit.vullevel_id).join(
                            Language, Language.id == Exploit.language_id).join(
                                Effect, Effect.id == Exploit.effect_id).join(
                                    User, User.id == Exploit.user_id).with_entities(
                                        Exploit.id, Exploit.name, Exploit.cve, VulType.name, Level.name, Effect.name, Application.name,
                                        Category.name, User.nickname)

        if form.page == -1:
            return json_response({
                'data': [x.to_json() for x in query.all()],
                'total': -1
            })
        if form.plugin_query.get('name'):
            query = query.filter(
                Exploit.name.like('%{}%'.format(form.plugin_query['name'])))

        if form.plugin_query.get('vul_type_id'):
            query = query.filter(Exploit.vul_type_id ==
                                 form.plugin_query.get('vul_type_id'))

        if form.plugin_query.get('level_id'):
            query = query.filter(Exploit.vullevel_id ==
                                 form.plugin_query.get('level_id'))

        if form.plugin_query.get('effect_id'):
            query = query.filter(Exploit.effect_id ==
                                 form.plugin_query.get('effect_id'))

        if form.plugin_query.get('application_id'):
            query = query.filter(Exploit.application_id ==
                                 form.plugin_query.get('application_id'))

        if form.plugin_query.get('category_id'):
            query = query.filter(Exploit.category_id ==
                                 form.plugin_query.get('category_id'))

        query = query.filter(Exploit.user_id == g.user.id).order_by(Exploit.id.desc())

        result = query.limit(form.pagesize).offset(
            (form.page - 1) * form.pagesize).all()
        return json_response({
            'data': [dict(zip(['id', 'exploit_name', 'cve', 'vultype_name', 'level_name', 'effect_name', 'application_name', 'category_name',
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


@blueprint.route('/levels', methods=['GET'])
@require_permission('exploit_view')
def search_levels():
    query = Level.query
    levels = query.all()
    total = query.count()
    return json_response({'data': [x.to_json() for x in levels], 'total': total})


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
            upload_path = "./upload/"+str(g.user.id)+"/"
            if not os.path.exists(upload_path):
                os.mkdir(upload_path)
            file.save(os.path.join(upload_path, alise_name))
            return json_response({"status": "上传成功", "file_list": [{"name": file.filename, "path": os.path.join(upload_path, alise_name)}]})
        except Exception:
            return json_response(message="上传失败")
    else:
        return json_response(message="只能上传txt文件")


@blueprint.route('/index', methods=['POST'])
@require_permission('exploit_add')
def post():
    args = AttrDict(name=Argument('name', type=str, help='请输入漏洞插件名称!'),
                    cve=Argument('cve', type=str, help='请输入漏洞编号!'),
                    vul_type_id=Argument(
                        'vul_type_id', type=str, help='请选择漏洞类型!'),
                    vullevel_id=Argument('vullevel_id', type=int, help='请选择危害等级!'),
                    effect_id=Argument('effect_id', type=int, help='请选择利用效果!'),
                    application_id=Argument(
                        'application_id', type=int, help='请选择应用名称！'),
                    category_id=Argument(
                        'category_id', type=int, help='请选择应用归类！'),
                    affect_version=Argument(
                        'affect_version', type=str, help='请输入目标版本!'),
                    language_id=Argument(
                        'language_id', type=int, help='请选择应用归类！'),
                    os=Argument('os', type=str, help='请输入目标系统!'),
                    desc=Argument('desc', type=str, help='请输入漏洞描述!'))
    form, error = JsonParser(*args.values()).parse()
    if error is None:
        if Exploit.query.filter(Exploit.name == form.name).first():
            return json_response(message='漏洞插件名称不能重复！')
        plugin = Exploit(**form)
        plugin.enter_time = datetime.now()
        plugin.update_time = ""
        plugin.user_id = g.user.id
        plugin.save()
        return json_response(plugin)
    return json_response(message=error)


@blueprint.route('/plugins/<int:plugin_id>', methods=['DELETE'])
@require_permission('publish_app_del')
def delete(plugin_id):
    plugin = Exploit.query.get_or_404(plugin_id)
    plugin.delete()
    return json_response()


@blueprint.route('/plugins/<int:plugin_id>', methods=['PUT'])
@require_permission('publish_app_edit')
def put(plugin_id):
    args = AttrDict(name=Argument('name', type=str, help='请输入漏洞插件名称!'),
                    cve=Argument('cve', type=str, help='请输入漏洞编号!'),
                    vul_type_id=Argument(
                        'vul_type_id', type=str, help='请选择漏洞类型!'),
                    vullevel_id=Argument('vullevel_id', type=int, help='请选择危害等级!'),
                    effect_id=Argument('effect_id', type=int, help='请选择利用效果!'),
                    application_id=Argument(
                        'application_id', type=int, help='请选择应用名称！'),
                    category_id=Argument(
                        'category_id', type=int, help='请选择应用归类！'),
                    affect_version=Argument(
                        'affect_version', type=str, help='请输入目标版本!'),
                    language_id=Argument(
                        'language_id', type=int, help='请选择应用归类！'),
                    os=Argument('os', type=str, help='请输入目标系统!'),
                    desc=Argument('desc', type=str, help='请输入漏洞描述!'))
    form, error = JsonParser(*args.values()).parse()
    if error is None:
        exists_record = Exploit.query.filter(Exploit.name == form.name).first()
        if exists_record and exists_record.id != plugin_id:
            return json_response(message='漏洞插件名称不能重复！')
        plugin = Exploit.query.get_or_404(plugin_id)
        plugin.update(**form)
        plugin.save()
        return json_response(plugin)
    return json_response(message=error)
