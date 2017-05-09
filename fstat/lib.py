from datetime import datetime, timedelta


def x_days_ago(x=1):
    '''
    Return timestamp for X days ago
    '''
    return (datetime.today().replace(hour=0, minute=0, second=0,
            microsecond=0) - timedelta(days=x))


def x_weeks_ago(x=1):
    '''
        Return timestamp for X weeks ago
    '''
    today = datetime.today().replace(hour=0, minute=0, second=0,
                                     microsecond=0)
    last_monday = today - timedelta(days=today.weekday())
    return last_monday - timedelta(days=x)
