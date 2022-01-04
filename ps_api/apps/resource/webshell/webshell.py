from flask import Blueprint, request, g, send_from_directory
import os
import time
from apps.resource.webshell.models import WebShell
from apps.account.models import User
# from apps.configuration.models import ConfigKey, AppConfigRel, Environment
# from apps.assets.models import Host
from libs.tools import json_response, JsonParser, Argument, AttrDict
# from libs.utils import Container
# from docker.errors import DockerException
from datetime import datetime
# from public import db
from libs.decorators import require_permission
# from apps.deploy.utils import get_built_in_menus

blueprint = Blueprint(__name__, __name__)


@blueprint.route('/plugin_download_check/<int:plugin_id>', methods=['GET'])
@require_permission('exploit_view')
def plugin_download_check(plugin_id):
    query = Exploit.query.filter(Exploit.id == plugin_id)
    plugin = query.first()
    if os.path.exists(plugin.plugin_file_path):
        return json_response(data={"msg": "漏洞插件即将开始下载"})
    else:
        return json_response(message="漏洞插件不存在")


@blueprint.route('/docker_download/<int:plugin_id>', methods=['GET'])
@require_permission('exploit_view')
def docker_download(plugin_id):
    query = Exploit.query.filter(Exploit.id == plugin_id)
    plugin = query.first()
    if os.path.exists(plugin.docker_file_path):
        try:
            filePath = plugin.docker_file_path.rsplit("/", 1)[0]
            filename = plugin.docker_file_path.rsplit("/", 1)[1]
            attachment_filename = filename.split("_", 1)[1]
            return send_from_directory(filePath, filename, as_attachment=True, attachment_filename=attachment_filename)
        except Exception as e:
            return json_response(message=str(e))
    else:
        return json_response(message="漏洞Docker虚拟环境不存在")


@blueprint.route('/standalone_tool_download/<int:plugin_id>', methods=['GET'])
@require_permission('exploit_view')
def standalone_tool_download(plugin_id):
    query = Exploit.query.filter(Exploit.id == plugin_id)
    plugin = query.first()
    if os.path.exists(plugin.standalone_tool_file_path):
        try:
            filePath = plugin.standalone_tool_file_path.rsplit("/", 1)[0]
            filename = plugin.standalone_tool_file_path.rsplit("/", 1)[1]
            attachment_filename = filename.split("_", 1)[1]
            return send_from_directory(filePath, filename, as_attachment=True, attachment_filename=attachment_filename)
        except Exception as e:
            return json_response(message=str(e))
    else:
        return json_response(message="漏洞独立利用工具不存在")


@blueprint.route('/plugin_download/<int:plugin_id>', methods=['GET'])
@require_permission('exploit_view')
def plugin_download(plugin_id):
    query = Exploit.query.filter(Exploit.id == plugin_id)
    plugin = query.first()
    if os.path.exists(plugin.plugin_file_path):
        try:
            filePath = plugin.plugin_file_path.rsplit("/", 1)[0]
            filename = plugin.plugin_file_path.rsplit("/", 1)[1]
            attachment_filename = filename.split("_", 1)[1]
            return send_from_directory(filePath, filename, as_attachment=True, attachment_filename=attachment_filename)
        except Exception as e:
            return json_response(message=str(e))
    else:
        return json_response(message="漏洞插件不存在")


@blueprint.route('/docker_remove', methods=['POST'])
@require_permission('exploit_view')
def docker_remove():
    form, error = JsonParser(
        Argument('name', type=str),
        Argument('path', type=str)
    ).parse()
    if os.path.exists(form.path):
        query = Exploit.query.filter(Exploit.docker_file_path == form.path)
        count = query.count()
        if count == 0:
            try:
                os.remove(form.path)
                return json_response(data={"status": "Docker虚拟环境删除成功"})
            except Exception:
                return json_response(message="Docker虚拟环境删除失败")
        else:
            return json_response(data={"status": "Docker虚拟环境删除成功"})
    else:
        return json_response(data={"status": "Docker虚拟环境删除成功"})


@blueprint.route('/docker_upload', methods=['POST'])
@require_permission('exploit_view')
def docker_upload():
    file = request.files['docker_file']
    if file.filename.rsplit('.', 1)[1].lower() == "zip" or file.filename.rsplit('.', 1)[1].lower() == "rar":
        try:
            alise_name = str(int(time.time()))+"_"+file.filename
            upload_path = "./upload/"+str(g.user.id)+"/dockers/"
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            file.save(os.path.join(upload_path, alise_name))
            return json_response({"status": "Docker虚拟环境上传成功", "file_list": [{"name": file.filename, "path": os.path.join(upload_path, alise_name)}]})
        except Exception:
            return json_response(message="Docker虚拟环境上传失败")
    else:
        return json_response(message="只能上传zip或rar文件")


@blueprint.route('/standalone_tool_remove', methods=['POST'])
@require_permission('exploit_view')
def standalone_tool_remove():
    form, error = JsonParser(
        Argument('name', type=str),
        Argument('path', type=str)
    ).parse()
    if os.path.exists(form.path):
        query = Exploit.query.filter(Exploit.standalone_tool_file_path == form.path)
        count = query.count()
        if count == 0:
            try:
                os.remove(form.path)
                return json_response(data={"status": "独立利用工具删除成功"})
            except Exception:
                return json_response(message="独立利用工具删除失败")
        else:
            return json_response(data={"status": "独立利用工具删除成功"})
    else:
        return json_response(data={"status": "独立利用工具删除成功"})


@blueprint.route('/standalone_tool_upload', methods=['POST'])
@require_permission('exploit_view')
def standalone_tool_upload():
    file = request.files['standalone_tool_file']
    if file.filename.rsplit('.', 1)[1].lower() == "zip" or file.filename.rsplit('.', 1)[1].lower() == "rar":
        try:
            alise_name = str(int(time.time()))+"_"+file.filename
            upload_path = "./upload/"+str(g.user.id)+"/standalone-tools/"
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            file.save(os.path.join(upload_path, alise_name))
            return json_response({"status": "独立利用工具上传成功", "file_list": [{"name": file.filename, "path": os.path.join(upload_path, alise_name)}]})
        except Exception:
            return json_response(message="独立利用工具上传失败")
    else:
        return json_response(message="只能上传zip或rar文件")


@blueprint.route('/plugin_remove', methods=['POST'])
@require_permission('exploit_view')
def plugin_remove():
    form, error = JsonParser(
        Argument('name', type=str),
        Argument('path', type=str)
    ).parse()
    if os.path.exists(form.path):
        query = Exploit.query.filter(Exploit.plugin_file_path == form.path)
        count = query.count()
        if count == 0:
            try:
                os.remove(form.path)
                return json_response(data={"status": "插件删除成功"})
            except Exception:
                return json_response(message="插件删除失败")
        else:
            return json_response(data={"status": "插件删除成功"})
    else:
        return json_response(data={"status": "插件删除成功"})


@blueprint.route('/plugin_upload', methods=['POST'])
@require_permission('exploit_view')
def plugin_upload():
    file = request.files['plugin_file']
    if file.filename.rsplit('.', 1)[1].lower() == "py":
        try:
            alise_name = str(int(time.time()))+"_"+file.filename
            upload_path = "./upload/"+str(g.user.id)+"/plugins/"
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            file.save(os.path.join(upload_path, alise_name))
            return json_response({"status": "插件上传成功", "file_list": [{"name": file.filename, "path": os.path.join(upload_path, alise_name)}]})
        except Exception as e:
            return json_response(message="插件上传失败."+str(e))
    else:
        return json_response(message="只能上传py文件")


@blueprint.route('/plugins/<int:plugin_id>/extend', methods=['GET'])
@require_permission('exploit_view')
def get_extend(plugin_id):
    query = Exploit.query.join(
            Category, Category.id == Exploit.category_id).join(
                VulType, VulType.id == Exploit.vul_type_id).join(
                    Application,
                    Application.id == Exploit.application_id).join(
                        Level, Level.id == Exploit.vullevel_id).join(
                            Language, Language.id == Exploit.language_id).join(
                                Effect, Effect.id == Exploit.effect_id).join(
                                    User, User.id == Exploit.user_id).with_entities(
                                        Exploit.affect_version, Exploit.enter_time, Exploit.update_time, Language.name, Exploit.os,
                                        Exploit.desc, Exploit.plugin_file_path, Exploit.standalone_tool_file_path, Exploit.docker_file_path,
                                        Exploit.virtual_machine_remarks).filter(
                                            Exploit.id == plugin_id)
    plugin_info = dict(zip(['affect_version', 'enter_time', 'update_time', 'language_name', 'os', 'desc', 'plugin_file_path',
                       'standalone_tool_file_path', 'docker_file_path', 'virtual_machine_remarks'], list(query.first())))
    if plugin_info["plugin_file_path"] and os.path.exists(plugin_info["plugin_file_path"]):
        plugin_info["plugin_file_name"] = plugin_info["plugin_file_path"].split("_", 1)[1]
    else:
        plugin_info["plugin_file_name"] = ""
    if plugin_info["standalone_tool_file_path"] and os.path.exists(plugin_info["standalone_tool_file_path"]):
        plugin_info["standalone_tool_file_name"] = plugin_info["standalone_tool_file_path"].split("_", 1)[1]
    else:
        plugin_info["standalone_tool_file_name"] = ""
    if plugin_info["docker_file_path"] and os.path.exists(plugin_info["docker_file_path"]):
        plugin_info["docker_file_name"] = plugin_info["docker_file_path"].split("_", 1)[1]
    else:
        plugin_info["docker_file_name"] = ""
    plugin_info.pop("plugin_file_path")
    plugin_info.pop("standalone_tool_file_path")
    plugin_info.pop("docker_file_path")
    return json_response(data=plugin_info)


@blueprint.route('/plugins/<int:plugin_id>', methods=['GET'])
@require_permission('exploit_view')
def get_plugin(plugin_id):
    vul = Exploit.query.get_or_404(plugin_id)
    if vul.plugin_file_path and not os.path.exists(vul.plugin_file_path):
        vul.plugin_file_path = ""
    if vul.standalone_tool_file_path and not os.path.exists(vul.standalone_tool_file_path):
        vul.standalone_tool_file_path = ""
    if vul.docker_file_path and not os.path.exists(vul.docker_file_path):
        vul.docker_file_path = ""
    return json_response(data=vul)


@blueprint.route('', methods=['GET'])
@require_permission('exploit_view')
def get():
    form, error = JsonParser(
        Argument('page', type=int, default=1, required=False),
        Argument('pagesize', type=int, default=10, required=False),
        Argument('webshell_query', type=dict, default={}),
    ).parse(request.args)
    if error is None:
        query = WebShell.query
        if form.webshell_query.get('target'):
            query = query.filter(WebShell.url.like('%{}%'.format(form.webshell_query.get("target"))))

        if form.plugin_query.get('public') != "":
            query = query.filter(WebShell.public == form.plugin_query.get("public"))

        query = query.filter(WebShell.user_id == g.user.id).order_by(WebShell.id.desc())

        result = query.limit(form.pagesize).offset(
            (form.page - 1) * form.pagesize).all()
        return json_response({
            'data': [dict(zip(['id', 'url', 'cve', 'pass', 'access_tool', 'public'], list(x))) for x in result],
            'total': query.count()
        })
    return json_response(message=error)


@blueprint.route('/vultypes', methods=['GET'])
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
    return json_response({'data': [x.to_json() for x in languages], 'total': total})


@blueprint.route('/plugins', methods=['POST'])
@require_permission('exploit_add')
def post():
    args = AttrDict(name=Argument('name', type=str, help='请输入漏洞名称!'),
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
                        'language_id', type=int, help='请选择应用语言！'),
                    os=Argument('os', type=str, help='请输入目标系统!'),
                    desc=Argument('desc', type=str, help='请输入漏洞描述!'),
                    plugin_file_path=Argument('plugin_file_path', type=str, help='请上传漏洞插件!'),
                    standalone_tool_file_path=Argument('standalone_tool_file_path', type=str, help='请上传漏洞独立利用工具!'),
                    docker_file_path=Argument('docker_file_path', required=False, type=str),
                    virtual_machine_remarks=Argument(
                        'virtual_machine_remarks', required=False, type=str),
                    )
    form, error = JsonParser(*args.values()).parse()
    if error is None:
        if Exploit.query.filter(Exploit.name == form.name).first():
            return json_response(message='漏洞插件名称不能重复！')
        plugin = Exploit(**form)
        plugin.enter_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        plugin.update_time = ""
        plugin.user_id = g.user.id
        plugin.save()
        return json_response(plugin)
    return json_response(message=error)


@blueprint.route('/plugins/<int:plugin_id>', methods=['DELETE'])
@require_permission('publish_app_del')
def delete(plugin_id):
    plugin = Exploit.query.get_or_404(plugin_id)
    if plugin.plugin_file_path and os.path.exists(plugin.plugin_file_path):
        try:
            os.remove(plugin.plugin_file_path)
        except Exception:
            return json_response(message="漏洞删除失败")
    if plugin.standalone_tool_file_path and os.path.exists(plugin.standalone_tool_file_path):
        try:
            os.remove(plugin.standalone_tool_file_path)
        except Exception:
            return json_response(message="漏洞删除失败")
    if plugin.docker_file_path and os.path.exists(plugin.docker_file_path):
        try:
            os.remove(plugin.docker_file_path)
        except Exception:
            return json_response(message="漏洞删除失败")
    plugin.delete()
    return json_response(data={"msg": "漏洞删除成功"})


@blueprint.route('/plugins/<int:plugin_id>', methods=['PUT'])
@require_permission('publish_app_edit')
def put(plugin_id):
    args = AttrDict(name=Argument('name', type=str, help='请输入漏洞名称!'),
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
                    desc=Argument('desc', type=str, help='请输入漏洞描述!'),
                    plugin_file_path=Argument('plugin_file_path', type=str, help='请上传漏洞插件!'),
                    standalone_tool_file_path=Argument('standalone_tool_file_path', type=str, help='请上传漏洞独立利用工具!'),
                    docker_file_path=Argument('docker_file_path', required=False, type=str),
                    virtual_machine_remarks=Argument('virtual_machine_remarks', required=False, type=str)
                    )
    form, error = JsonParser(*args.values()).parse()
    if error is None:
        exists_record = Exploit.query.filter(Exploit.name == form.name).first()
        if exists_record and exists_record.id != plugin_id:
            return json_response(message='漏洞插件名称不能重复！')
        plugin = Exploit.query.get_or_404(plugin_id)
        if plugin.plugin_file_path and plugin.plugin_file_path != form.plugin_file_path:
            if os.path.exists(plugin.plugin_file_path):
                try:
                    os.remove(plugin.plugin_file_path)
                except Exception:
                    return json_response(message="插件更新失败")

        if plugin.standalone_tool_file_path and plugin.standalone_tool_file_path != form.standalone_tool_file_path:
            if os.path.exists(plugin.standalone_tool_file_path):
                try:
                    os.remove(plugin.standalone_tool_file_path)
                except Exception:
                    return json_response(message="插件更新失败")

        if plugin.docker_file_path and plugin.docker_file_path != form.docker_file_path:
            if os.path.exists(plugin.docker_file_path):
                try:
                    os.remove(plugin.docker_file_path)
                except Exception:
                    return json_response(message="插件更新失败")
        plugin.update(**form)
        plugin.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        plugin.save()
        return json_response(plugin)
    return json_response(message=error)
