from collections import Counter

from flask import render_template, redirect, url_for, request

from fstat import app, db
from fstat.lib import x_days_ago
from fstat.model import Failure, FailureInstance


@app.route("/")
def index():
    return redirect(url_for('overall_summary'))


@app.route('/summary')
def overall_summary():
    '''
    Shows overall summary
    Params
    start_day: date with format yyyy-mm-dd, if start date is none it is defaulted to the last monday
    end_day: date with format yyyy-mmd-dd, if end date is none it is defaulted to today
    '''
    start_date = parse_start_date(request.args.get('start_date'))
    end_date = parse_end_date(request.args.get('end_date'))

    failure_instances = FailureInstance.query.filter(FailureInstance.timestamp > start_date,
                                                     FailureInstance.timestamp < end_date)
    failures = Counter([x.failure for x in failure_instances])
    return render_template('index.html',
                           num=(end_date - start_date).days,
                           failures=failures,
                           total=len(failures),
                           end_date=str(end_date.date()),
                           start_date=str(start_date.date()),
                           )


@app.route('/failure/<int:fid>')
def instance_summary(fid=None):
    '''
    Shows instance summary for particular failure
    Params
    start_day: date with format yyyy-mm-dd, if start date is none it is defaulted to the last monday
    end_day: date with format yyyy-mm-dd, if end date is none it is defaulted to today
    '''
    fid = int(fid)
    start_date = parse_start_date(request.args.get('start_date'))
    end_date = parse_end_date(request.args.get('end_date'))

    failure = Failure.query.filter_by(id=fid).first_or_404()
    failure_instances = FailureInstance.query.filter(db.and_(FailureInstance.timestamp > start_date,
                                                             FailureInstance.timestamp < end_date,
                                                             FailureInstance.failure == failure))
    return render_template('failure_instance.html',
                           failure=failure,
                           failure_instances=failure_instances,
                           end_date=str(end_date.date()),
                           start_date=str(start_date.date()),
                           title="Summary for " + failure.signature)
