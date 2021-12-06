from public import db
from libs.model import ModelMixin


class Task(db.Model, ModelMixin):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    url_list = db.Column(db.Text)
    plugins = db.Column(db.Text)
    desc = db.Column(db.String(255))
    url_file_path = db.Column(db.String(255))
    start_time = db.Column(db.String(255))
    create_time = db.Column(db.String(255))
    update_time = db.Column(db.String(255))
    user_id = db.Column(db.ForeignKey('account_users.id', ondelete='CASCADE'))
    finish_time = db.Column(db.String(255))
    exec_model_id = db.Column(db.ForeignKey('exec_model.id', ondelete='CASCADE'))
    status = db.Column(db.Integer)

    def __repr__(self):
        return '<Task name=%r>' % (self.name)


class TaskDetail(db.Model, ModelMixin):
    __tablename__ = 'task_detail'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    target = db.Column(db.String(255))
    vul_id = db.Column(db.ForeignKey('exploit.id', ondelete='CASCADE'))
    status = db.Column(db.Integer)
    task_id = db.Column(db.ForeignKey('task.id', ondelete='CASCADE'))
    user_id = db.Column(db.ForeignKey('account_users.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<Task name=%r>' % (self.name)


class ExecModel(db.Model, ModelMixin):
    __tablename__ = 'exec_model'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return '<ExecModel %r>' % self.name
