from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from concurrent.futures import ThreadPoolExecutor
import config
from flask_simpleldap import LDAP
from libs.pocstrike.lib.core.common import set_paths
import os

app = Flask(__name__)
app.config.from_object(config)

app.config['LDAP_BASE_DN'] = app.config['LDAP_CONFIG'].get('base_dn')
app.config['LDAP_USERNAME'] = app.config['LDAP_CONFIG'].get('admin_dn')
app.config['LDAP_PASSWORD'] = app.config['LDAP_CONFIG'].get('admin_password')
app.config['LDAP_OPENLDAP'] = app.config['LDAP_CONFIG'].get('is_openldap')
app.config['LDAP_USER_OBJECT_FILTER'] = '(&(objectclass=inetOrgPerson)({0}=%s))'\
    .format(app.config['LDAP_CONFIG'].get('user_filter'))
app.config['LDAP_HOST'] = app.config['LDAP_CONFIG'].get('host')
app.config['LDAP_PORT'] = app.config['LDAP_CONFIG'].get('port')


db = SQLAlchemy(app)
ldap = LDAP(app)
executor = ThreadPoolExecutor(20)


def module_path():
    """
    This will get us the program's directory
    """
    return os.path.dirname(os.path.realpath(__file__))+"\\libs\\pocstrike"


def check_environment():
    try:
        os.path.isdir(module_path())
    except Exception:
        err_msg = "your system does not properly handle non-ASCII paths. "
        err_msg += "Please move the pocstrike's directory to the other location"
        raise SystemExit


check_environment()
set_paths(module_path())
