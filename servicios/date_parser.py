import datetime

def parse_dd_mm_yyyy(str_date,separator="/"):
    return datetime.datetime.strptime( str_date,f"%d{separator}%m{separator}%Y").date()