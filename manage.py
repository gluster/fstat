#!/usr/bin/env python

from flask_script import Server, Manager
from flask_migrate import MigrateCommand

from fstat import app
from fstat.parser import get_summary


manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('db', MigrateCommand)


@manager.option('-n', dest='num_days')
@manager.option('-j', '--job', dest='job_name')
def process_jobs(job_name, num_days):
    get_summary(job_name, int(num_days))


if __name__ == '__main__':
    manager.run()
