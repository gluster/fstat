# Fstat [![Build Status](https://travis-ci.org/gluster/fstat.svg?branch=master)](https://travis-ci.org/gluster/fstat)
Fstat tracks the failures from build.gluster.org.

## Installation
- Before you start installation make sure you have a working installation of python2
- Create virtualenv ``` virtualenv venv ```
- Activate virtualenv ``` source venv/bin/activate ```
- In your virtualenv run ``` pip install -r requirements.txt ```
- Hurray the installation is done

## Using fstat
- Run migrations and setup database ``` python manage.py db upgrade ```
- To serve the fstat app on localhost run ``` python manage.py runserver ```
- Create application.cfg and add ``` DEBUG=True ``` to it to enable debug mode for your flask app.
- To fetch failures from build.gluster.org run ``` python manage.py proccess_jobs -n <number_of_days> -j <job_name> ```
- By default fstat reads and writes the data into sqlite but it can be overriden in your application.cfg.

## Consuming fstat data via rest apis

###  ``` /api/failures ```
This endpoint is used to get list of failures with the number of failure instances. The available filters for this endpoint are as follows:

**Name**|**Description**
:-----:|:-----:
start\_date| The date from which you want to get the failures (format yyyy-mm-dd)
end\_date| The date till which you want to get the failures (format yyyy-mm-dd)
branch| filter for specific branch

For Eg:

```
GET /api/failures?start_date=2017-05-01&end_date=2017-08-01&branch=master
```

### ``` /api/failures/<fid> ```
This endpoint will return the list of failure instances for a particular failureID, this failure id is specific to fstat. The available filters for this endpoint are as follows:

**Name**|**Description**
:-----:|:-----:
start\_date| The date from which you want to get the failures (format yyyy-mm-dd)
end\_date| The date till which you want to get the failures (format yyyy-mm-dd)
branch| filter for specific branch

For Eg:

```
GET /api/failures/1?start_date=2017-05-01&end_date=2017-08-01&branch=master
```
