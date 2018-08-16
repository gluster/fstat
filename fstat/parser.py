import re
from datetime import timedelta, datetime
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from sqlalchemy.exc import IntegrityError
from fstat import app, db, Failure, FailureInstance


TYPE = {
    'NONE': 0,
    'FAILURE': 1,
    'TIMEOUT': 2,
}


class FailureParser(object):

    def __init__(self, build_info, job_name):
        self.url = ''.join([build_info['url'], 'consoleText'])
        self.job_name = job_name
        self.build_info = build_info

    def is_parsed(self):
        if FailureInstance.query.filter_by(url=self.url).first():
            return True
        return False

    def process_failure(self):
        if self.is_parsed():
            return
        text = requests.get(self.url, verify=False).text
        for line in text.split('\n'):
            # Failures are in this form:
            # something.t (Wstat: 0 Tests: 26 Failed: 2)
            #   Failed tests:  15, 22
            # Files=1, Tests=26....
            # Result: FAIL
            #
            # Every test we find goes into a variable called test_line first
            if line.find("Wstat") != -1:
                test_line = line

            # If we find a line with failure, that means the test in the line we
            # wrote to test_line failed.
            if line.find("Result: FAIL") != -1:
                test_case = re.search(r'\./tests/.*\.t', test_line)
                if test_case:
                    self.save_failure(test_case.group(), type='FAILURE')
            # If the test timed out the output looks like this:
            #
            # [20:43:46] Running tests in file something.t
            # Timeout set is 800, default 200
            # something.t timed out after 800 seconds
            # something.t: bad status 124

            if line.find("timed out after") != -1:
                test_case = re.search(r'\./tests/.*\.t', line)
                if test_case:
                    self.save_failure(test_case.group(), type='TIMEOUT')

    def save_failure(self, signature, type=None):
        failure = Failure.query.filter_by(signature=signature).first()
        # If it doesn't exist, create a job first
        if failure is None:
            failure = Failure(signature=signature)
            failure.type = TYPE[type]

        failure_instance = FailureInstance(url=self.url,
                                           job_name=self.job_name)
        failure_instance.process_build_info(self.build_info)
        failure_instance.failure = failure
        try:
            db.session.add(failure)
            db.session.add(failure_instance)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


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
                failure = FailureParser(build, job_name)
                failure.process_failure()
