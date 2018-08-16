import factory
from datetime import datetime

from fstat import app, db
from fstat.model import Failure, FailureInstance

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'


class FailureFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Failure
        sqlalchemy_session = db.session

    signature = factory.Faker('text')
    type = 1


class FailureInstanceFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = FailureInstance
        sqlalchemy_session = db.session

    url = factory.Faker('text')
    timestamp = datetime.now().replace(day=datetime.today().day - 1)
    job_name = 'regression-test-burn-in'
    branch = 'master'
    failure = factory.SubFactory(FailureFactory)


with app.app_context():
    db.create_all()

    for i in range(10):
        failure = FailureFactory()
        db.session.commit()
    for i in range(10):
        failure_instance = FailureInstanceFactory()
        db.session.commit()
