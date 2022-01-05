import datetime

friday = datetime.datetime.today()
while friday.weekday() != 4:
    friday += datetime.timedelta(1)

friday_datetime = datetime.datetime(friday.year, friday.month, friday.day)