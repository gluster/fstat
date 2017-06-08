from collections import Counter

from flask import render_template, redirect, url_for, request, session, g, jsonify

from fstat import app, db, github
from model import Failure, FailureInstance, User
from lib import parse_end_date, parse_start_date, get_branch_list


@github.access_token_getter
def token_getter():
    return session['token']


@app.before_request
def before_request():
    if 'token' in session:
        user = User.query.filter_by(token=session['token']).first()
        g.user = user


@app.route("/")
def index():
    return redirect(url_for('overall_summary'))


@app.route('/login', methods=['POST'])
def login():
    return github.authorize(scope="user:email,read:org")


@app.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    session['token'] = oauth_token
    if oauth_token:
        response_user_data = github.get('user')
        user = User.query.filter_by(email=response_user_data['email']).first()
        if not user:
            user = User()
            user.email = response_user_data['email']
            user.username = response_user_data['login']
            user.name = response_user_data['name']
            user.profile_picture = response_user_data['avatar_url']
            user.token = oauth_token
            db.session.add(user)
        user.token = oauth_token
        db.session.commit()
    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/summary')
@app.route('/api/failures', endpoint='api:failures')
def overall_summary():
    '''
    Shows overall summary
    Params
    start_day: date with format yyyy-mm-dd, if start date is none it is defaulted to the last monday
    end_day: date with format yyyy-mmd-dd, if end date is none it is defaulted to today
    '''
    start_date = parse_start_date(request.args.get('start_date'))
    end_date = parse_end_date(request.args.get('end_date'))
    branch = request.args.get('branch', 'all')

    filters = [
        FailureInstance.timestamp > start_date,
        FailureInstance.timestamp < end_date
    ]

    if branch != 'all':
        filters.append(FailureInstance.branch == branch)

    failure_instances = FailureInstance.query.filter(*filters)

    failures = Counter([x.failure for x in failure_instances])
    if request.endpoint == 'api:failures':
        failures_ = []
        for failure, count in failures.most_common():
            failures_.append({
                "signature": "http://git.gluster.org/cgit/glusterfs.git/tree/" + failure.signature,
                "count": count
            })
        return jsonify({"response": failures_})

    return render_template('index.html',
                           num=(end_date - start_date).days,
                           failures=failures,
                           total=len(failures),
                           end_date=str(end_date.date()),
                           start_date=str(start_date.date()),
                           branches=get_branch_list())


@app.route('/failure/<int:fid>')
@app.route('/api/failure/<int:fid>', endpoint='api:failure_instances')
def instance_summary(fid=None):
    '''
    Shows instance summary for particular failure
    Params
    start_day: date with format yyyy-mm-dd, if start date is none it is defaulted to the last monday
    end_day: date with format yyyy-mm-dd, if end date is none it is defaulted to today
    branch: name of branch
    '''
    fid = int(fid)
    start_date = parse_start_date(request.args.get('start_date'))
    end_date = parse_end_date(request.args.get('end_date'))
    branch = request.args.get('branch', 'all')

    failure = Failure.query.filter_by(id=fid).first_or_404()
    filters = [
        FailureInstance.timestamp > start_date,
        FailureInstance.timestamp < end_date,
        FailureInstance.failure == failure
    ]

    if branch != 'all':
        filters.append(FailureInstance.branch == branch)

    failure_instances = FailureInstance.query.filter(db.and_(*filters))
    if request.endpoint == 'api:failure_instances':
        failure_instances = [failure_instance.as_dict() for failure_instance in failure_instances]
        return jsonify({"response": failure_instances})

    return render_template('failure_instance.html',
                           failure=failure,
                           branches=get_branch_list(fid),
                           failure_instances=failure_instances,
                           end_date=str(end_date.date()),
                           start_date=str(start_date.date()),
                           title="Summary for " + failure.signature)
