from pytz import timezone
import os
from datetime import timedelta

DEBUG = True
TIME_ZONE = timezone('Asia/Shanghai')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/pocstrike'
SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_POOL_RECYCLE = 90
SQLALCHEMY_POOL_TIMEOUT = 100
DOCKER_REGISTRY_SERVER = 'hub.qbangmang.com'
DOCKER_REGISTRY_AUTH = {'username': 'hubuser', 'password': 'hubpassword'}

LDAP_CONFIG = {
    'host': '',
    'port': 389,
    'is_openldap':  True,
    'base_dn': 'dc=spug,dc=com',
    'admin_dn': 'cn=admin,dc=spug,dc=com',
    'admin_password': 'spugpwd',
    'user_filter': 'cn',
}
