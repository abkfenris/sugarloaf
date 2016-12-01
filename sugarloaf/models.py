from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from geoalchemy2 import Geometry

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username


class Area(db.Model):
    __tablename__ = 'areas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __repr__(self):
        return '<Area {name}>'.format(name=self.name)


class Trail(db.Model):
    __tablename__ = 'trails'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    geom = db.Column(Geometry('LINESTRING', 4326))
    description = db.Column(db.Text)
    osm_id = db.Column(db.BigInteger)
    current = db.Column(db.Boolean, default=True)

    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'))
    area = db.relationship('Area', backref=db.backref('trails', lazy='dynamic'))

    def __repr__(self):
        return '<Trail {name}>'.format(name=self.name)


class TrailStatus(db.Model):
    __tablename__ = 'trail_status'

    id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.DateTime)
    open = db.Column(db.Boolean)
    groomed = db.Column(db.Boolean)
    snowmaking = db.Column(db.Boolean)

    trail_id = db.Column(db.Integer, db.ForeignKey('trails.id'))
    trail = db.relationship('Trail', backref=db.backref('statuses', lazy='dynamic'))


class Lift(db.Model):
    __tablename__ = 'lifts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    dt = db.Column(db.DateTime)
    description = db.Column(db.Text)
    geom = db.Column(Geometry('LINESTRING', 4326))


class LiftStatus(db.Model):
    __tablename__ = 'lift_status'

    id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.DateTime)
    running = db.Column(db.Boolean)
    scheduled = db.Column(db.Boolean)
    hold = db.Column(db.Boolean)

    lift_id = db.Column(db.Integer, db.ForeignKey('lifts.id'))
    lift = db.relationship('Lift', backref=db.backref('statuses', lazy='dynamic'))


class SnowReporter(db.Model):
    __tablename__ = 'snow_reporters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __repr__(self):
        return '<SnowReporter {name}>'.format(name=self.name)


class DailyReport(db.Model):
    __tablename__ = 'daily_reports'

    id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.DateTime)
    report = db.Column(db.Text)

    reporter_id = db.Column(db.Integer, db.ForeignKey('snow_reporters.id'))
    reporter = db.relationship('SnowReporter', 
                               backref=db.backref('reports', 
                                                  lazy='dynamic'))

