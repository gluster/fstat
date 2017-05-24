from datetime import datetime, timedelta

from fstat import db
from model import FailureInstance


def parse_start_date(start_date=None):
    if not start_date:
        today = datetime.today().replace(hour=0, minute=0, second=0,
                                         microsecond=0)
        start_date = today - timedelta(days=today.weekday())

        if (datetime.today() - start_date).days == 0:
            start_date = start_date - timedelta(days=7)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    return start_date


def parse_end_date(end_date=None):
    if not end_date:
        end_date = datetime.today()
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    return end_date


def get_branch_list(fid=None):
    if not fid:
        return db.session.query(FailureInstance.branch) \
                .filter(FailureInstance.branch.isnot(None)) \
                .order_by(FailureInstance.branch) \
                .distinct()
    else:
        return db.session.query(FailureInstance.branch) \
                .filter(FailureInstance.failure_id == fid,
                        FailureInstance.branch.isnot(None)) \
                .order_by(FailureInstance.branch) \
                .distinct()
