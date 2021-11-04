import re
from collections import OrderedDict

from libs.pocstrike.api \
    import Output, POCBase, POC_CATEGORY, register_poc, requests, VUL_TYPE, get_listener_ip, get_listener_port, random_str
from libs.pocstrike.lib.core.interpreter_option \
    import OptString, OptDict, OptIP, OptPort, OptBool, OptInteger, OptFloat, OptItems
from libs.pocstrike.modules.listener import REVERSE_PAYLOAD


class DemoPOC(POCBase):
    vulID = '1'                  # 漏洞ID
    version = '1'                   # 默认为1
    author = 'test'               # PoC作者
    vulDate = '2021-04-12'          # 漏洞公开的时间,不知道就写今天
    createDate = '2021-04-12'       # 编写 PoC 的日期
    updateDate = '2021-04-12'       # PoC 更新的时间,默认和编写时间一样
    references = ['https://xxx.xx.com.cn']      # 漏洞地址来源,0day不用写
    name = 'XXXX SQL注入漏洞 PoC'   # PoC 名称
    appPowerLink = 'https://www.xxx.org/'    # 漏洞厂商主页地址
    appName = 'XXXX'          # 漏洞应用名称
    appVersion = '1.x'          # 漏洞影响版本
    vulType = VUL_TYPE.UNAUTHORIZED_ACCESS      # 漏洞类型,类型参考见 漏洞类型规范表
    category = POC_CATEGORY.EXPLOITS.WEBAPP
    samples = []                # 测试样列,就是用 PoC 测试成功的网站
    install_requires = []       # PoC 第三方模块依赖，请尽量不要使用第三方模块
    desc = '''
            漏洞简要描述。
        '''                     # 漏洞简要描述
    pocDesc = '''
            poc的用法描述
        '''                     # POC用法描述

    def _options(self):
        opt = OrderedDict()     # value = self.get_option('key')
        opt["string"] = OptString('', description='这个poc需要用户登录，请输入登录账号', require=True)
        opt["integer"] = OptInteger('', description='这个poc需要用户密码，请输出用户密码', require=False)
        return opt

    def _verify(self):
        output = Output(self)
        result = {}
        # 验证代码
        .......

        result = {
            'Result': {
                'target': "http://192.168.1.19:8080",
                'webshell': "http://192.168.1.19:8080/1619330399.jsp?pwd=023&cmd=whoami",
                'site_username': 'admin',
                'site_pass': 'passwd',
                'a': 'a',
                'b': 'b'
            }
        }

        return self.parse_output(output, result)

    def _attack(self):
        output = Output(self)
        result = {}
        # 攻击代码
        .......

        result = {
            'Result': {
                'target': "http://192.168.1.19:8080",
                'webshell': "http://192.168.1.19:8080/1619330399.jsp?pwd=023&cmd=whoami",
                'site_username': 'admin',
                'site_pass': 'passwd',
                'a': 'a',
                'b': 'b'
            }
        }

        return self.parse_output(output, result)

    def _shell(self):
        pass

    def parse_output(self, output, result):
        if result:
            output.success(result)
        else:
            output.fail()
        return output


def other_fuc():
    pass


def other_utils_func():
    pass


# 注册 DemoPOC 类
register_poc(DemoPOC)
