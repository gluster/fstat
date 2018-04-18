import re
from datetime import timedelta, datetime
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from sqlalchemy.exc import IntegrityError
from fstat import app, db, Failure, FailureInstance


STATE = (
    None,
    'SUCCESS',
    'FAILURE',
    'ABORTED',
)


def save_failure(signature, url, job_name, build_info):
    failure = Failure.query.filter_by(signature=signature).first()
    # If it doesn't exist, create a job first
    if failure is None:
        failure = Failure(signature=signature)
        failure.state = STATE.index(build_info['result'])

    failure_instance = FailureInstance(url=url,
                                       job_name=job_name)
    failure_instance.process_build_info(build_info)
    failure_instance.failure = failure
    try:
        db.session.add(failure)
        db.session.add(failure_instance)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def process_failure(url, job_name, build_info):
    text = requests.get(url, verify=False).text
    accum = []
    if text.find("Build timed out") and build_info['result'] == 'ABORTED':
        lines = text.split('\n')
        # Reversing the array to catch the last ran test because of which the run got aborted
        lines.reverse()
        for line in lines:
            test_case = re.search(r'\./tests/.*\.t', line)
            if test_case:
                save_failure(test_case.group(), url, job_name, build_info)
                break
    else:
        for t in text.split('\n'):
            if t.find("Result: FAIL") != -1:
                for t2 in accum:
                    if t2.find("Wstat") != -1:
                        test_case = re.search(r'\./tests/.*\.t', t2)
                        if test_case:
                            save_failure(test_case.group(), url, job_name,
                                         build_info)
                accum = []
            if t.find("timed out after") != -1:
                test_case = re.search(r'\./tests/.*\.t', t)
                if test_case:
                    save_failure(test_case.group(), url, job_name, build_info)
            else:
                accum.append(t)


def get_summary(job_name, num_days):
    '''
    Get links to the failed jobs
    '''
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    cut_off_date = datetime.today() - timedelta(days=num_days)
    for page in xrange(0, app.config['JENKINS_MAX'], 100):
        build_info = requests.get(''.join([
            app.config['JENKINS_URL'],
            '/job/',
            job_name,
            '/'
            'api/json?depth=1&tree=allBuilds'
            '[url,result,timestamp,builtOn,actions[parameters[value]]]',
            '{{{0},{1}}}'.format(page, page+100)
        ]), verify=False).json()
        for build in build_info.get('allBuilds'):
            if datetime.fromtimestamp(build['timestamp']/1000) < cut_off_date:
                # stop when timestamp older than cut off date
                return
            if build['result'] not in [None, 'SUCCESS']:
                url = ''.join([build['url'], 'consoleText'])
                if not FailureInstance.query.filter_by(url=url).first():
                    process_failure(url, job_name, build)
