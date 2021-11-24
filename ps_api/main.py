from public import app
# from config import DEBUG
from libs import middleware
from apps import account
from apps import home
from apps import common
from apps import exploit
from apps import task

middleware.init_app(app)
account.register_blueprint(app)
home.register_blueprint(app)
common.register_blueprint(app)
exploit.register_blueprint(app)
task.register_blueprint(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
