"""

  """

import re
from datetime import datetime as dt
from datetime import time

from numpy import vectorize
from persiantools.jdatetime import JalaliDate


def persian_tools_jdate_from_int(jdate_int_fmt: {int , str}) :
    jd = jdate_int_fmt
    if not (isinstance(jd , str) or isinstance(jd , int)) :
        return jd

    jd = str(int(jd))
    int_fmt_jd = r'1[34]\d\d[0-2]\d[0-3]\d'
    cnd = re.fullmatch(int_fmt_jd , jd)

    if cnd is not None :
        return JalaliDate(int(jd[:4]) , int(jd[4 :6]) , int(jd[6 :8]))
    elif cnd is None :
        raise ValueError

def make_zero_padded_jdate_ie_iso_fmt(ist , sep = '/') :
    spl = ist.split(sep)
    for _i in range(1 , 3) :
        if int(spl[_i]) < 10 :
            spl[_i] = '0' + spl[_i]
    ou = '-'.join(spl)
    return ou

def make_datetime_from_iso_jdate_time(ist) :
    ptr = r'(\d{4})-(\d{2})-(\d{2})(\s*T?\s*)(\d{2}):(\d{2}):(\d{2})'
    cnd = re.fullmatch(ptr , ist)
    if cnd is None :
        raise ValueError

    jd = JalaliDate(int(cnd.group(1)) , int(cnd.group(2)) , int(cnd.group(3)))
    date = jd.to_gregorian()

    t = time(int(cnd.group(5)) , int(cnd.group(6)) , int(cnd.group(7)))

    date_time = dt.combine(date , t)
    return date_time

fu0 = make_datetime_from_iso_jdate_time
vect_make_datetime_from_iso_jdate_time = vectorize(fu0)
