''' Gets the last day of the month for filtering in cvai-mvp '''
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_month_lastday(aaa):
    return datetime.strptime(aaa,'%Y-%m-%d') + relativedelta(day=31)  # End-of-month

aaa = '2021-02-01'
print(get_month_lastday(aaa))