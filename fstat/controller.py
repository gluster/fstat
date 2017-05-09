from collections import Counter
from flask import render_template, redirect, url_for
from fstat import app, db
from fstat.lib import x_weeks_ago
from model import Failure, FailureInstance
from datetime import datetime


@app.route("/")
def index():
    return redirect(url_for('weekly_overall_summary', num=1))


@app.route("/weeks/<int:num>")
def weekly_overall_summary(num=None):
    if num > 12:
        num = 12
    cut_off_date = (x_weeks_ago(num*7))
    failure_instances = FailureInstance.query.filter(
            FailureInstance.timestamp > cut_off_date)
    failures = Counter([x.failure for x in failure_instances])
    return render_template('index.html',
                           num=num,
                           failures=failures,
                           total=len(failures),
                           cut_off=cut_off_date.strftime('%Y-%m-%d'),
                           today=datetime.today().strftime('%Y-%m-%d'),
                           )


@app.route("/weeks/<int:num>/failure/<int:fid>")
def weekly_instance_summary(num=None, fid=None):
    if num > 4:
        num = 4
    fid = int(fid)
    cut_off_date = (x_weeks_ago(num*7))
    print cut_off_date
    failure = Failure.query.filter_by(id=fid).first_or_404()
    failure_instances = FailureInstance.query.filter(
            db.and_(
                FailureInstance.timestamp > cut_off_date,
                FailureInstance.failure == failure))
    return render_template('failure_instance.html',
                           num=num,
                           failure=failure,
                           failure_instances=failure_instances,
                           cut_off=cut_off_date.strftime('%Y-%m-%d'),
                           today=datetime.today().strftime('%Y-%m-%d'),
                           title="Summary for " + failure.signature,
                           )
