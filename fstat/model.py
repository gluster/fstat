from fstat import db
from datetime import datetime


STATE = (
    None,
    'SUCCESS',
    'FAILURE',
    'ABORTED',
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    github_username = db.Column(db.Integer, unique=True)
    email = db.Column(db.String, unique=True)
    profile_picture = db.Column(db.String)
    token = db.Column(db.String)
    name = db.Column(db.String)


class Failure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    signature = db.Column(db.String(1000), index=True)
    failures = db.relationship('FailureInstance',
                               backref='failure',
                               lazy='dynamic')
    bugs = db.relationship('BugFailure', backref="failure")


class FailureInstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100), index=True)
    state = db.Column(db.Integer)
    job_name = db.Column(db.String(100), index=True)
    node = db.Column(db.String(100), index=True)
    timestamp = db.Column(db.DateTime, index=True)
    review = db.Column(db.Integer, index=True)
    patchset = db.Column(db.Integer)
    branch = db.Column(db.String(100), index=True)
    failure_id = db.Column(db.Integer, db.ForeignKey('failure.id'))
    __table__args = (db.UniqueConstraint(url, failure_id))

    def process_build_info(self, build):
        self.state = STATE.index(build['result'])
        self.node = build['builtOn']
        self.timestamp = datetime.fromtimestamp(build['timestamp']/1000)
        try:
            self.review = build['actions'][5]['parameters'][4]['value']
        except KeyError:
            pass
        try:
            self.patchset = build['actions'][5]['parameters'][6]['value']
        except KeyError:
            pass
        try:
            self.branch = build['actions'][5]['parameters'][2]['value']
        except KeyError:
            self.branch = 'master'


class BugFailure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    failure_id = db.Column(db.Integer, db.ForeignKey('failure.id'))
    bug_id = db.Column(db.Integer) #refers to the bug on bugzilla
    user_id = db.Column(db.Integer) #refers to the use who associate the bug
