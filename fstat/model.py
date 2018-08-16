from datetime import datetime
from fstat import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    profile_picture = db.Column(db.String(1000))
    token = db.Column(db.String(1000))
    name = db.Column(db.String(100))


class Failure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    signature = db.Column(db.String(1000), index=True)
    type = db.Column(db.Integer, default=1)
    failures = db.relationship('FailureInstance',
                               backref='failure',
                               lazy='dynamic')
    bugs = db.relationship('BugFailure', backref="failure")

    @staticmethod
    def get_bug_ids(fid):
        failure = Failure.query.filter_by(id=fid).first()
        return [bug.bug_id for bug in failure.bugs]


class FailureInstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100), index=True)
    job_name = db.Column(db.String(100), index=True)
    node = db.Column(db.String(100), index=True)
    timestamp = db.Column(db.DateTime, index=True)
    review = db.Column(db.Integer, index=True)
    patchset = db.Column(db.Integer)
    branch = db.Column(db.String(100), index=True)
    failure_id = db.Column(db.Integer, db.ForeignKey('failure.id'))
    __table__args = (db.UniqueConstraint(url, failure_id))

    def as_dict(self):
        return {
            "url": self.url,
            "job_name": self.job_name,
            "node": self.node,
            "timestamp": self.timestamp,
            "patchset": self.patchset,
            "branch": self.branch,
            "failure_id": self.failure_id
        }

    def process_build_info(self, build):
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
    failure_id = db.Column(db.Integer, db.ForeignKey('failure.id'), nullable=False)
    bug_id = db.Column(db.Integer, nullable=False)  # refers to the bug on bugzilla
    created_at = db.Column(db.DateTime, default=datetime.now)
