from public import db
from libs.model import ModelMixin


class WebShell(db.Model, ModelMixin):
    __tablename__ = 'webshell'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255))
    password = db.Column(db.String(255))
    access_tool = db.Column(db.String(255))
    public = db.Column(db.Integer)
    user_id = db.Column(db.ForeignKey('account_users.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<WebShell url=%r, password=%r>' % (self.url, self.password)
