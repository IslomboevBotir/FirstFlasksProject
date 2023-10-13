from flask_migrate import Migrate
from database import db, app


migrate = Migrate(app, db)


class DataBaseProject(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer)
    unit = db.Column(db.String(255))
    w_id = db.Column(db.Integer, unique=True)
    utype = db.Column(db.String(255))
    beds = db.Column(db.Integer)
    area = db.Column(db.Float)
    price = db.Column(db.Integer)
    date = db.Column(db.Date)
    is_mode = db.Column(db.Boolean)
    is_del = db.Column(db.Boolean)
