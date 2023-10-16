"""

  """

import datetime
import re
from datetime import datetime
from datetime import time

import pandas as pd
from numpy import vectorize
from persiantools.jdatetime import JalaliDate
from persiantools.jdatetime import JalaliDateTime

from .strr import convert_digits_to_en

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
            spl[_i] = '0' + str(int(spl[_i]))
    ou = '-'.join(spl)
    return ou

def make_persiantools_jdate_from_str(ist , sep = '-') :
    ist = make_zero_padded_jdate_ie_iso_fmt(ist , sep = sep)
    ist = ist.replace('-' , '')
    return persian_tools_jdate_from_int(ist)

def convert_str_jdate_to_date(ist: str , sep = '-') -> datetime.date :
    jd = make_persiantools_jdate_from_str(ist , sep = sep)
    return jd.to_gregorian()

def convert_jdate_to_date_from_str(ist , sep = '-') :
    jd = make_persiantools_jdate_from_str(ist , sep = sep)
    return jd.to_gregorian().isoformat()

def make_datetime_from_iso_jdate_time(ist) :
    ptr = r'(\d{4})-(\d{2})-(\d{2})(\s*T?\s*)(\d{2}):(\d{2}):(\d{2})'
    cnd = re.fullmatch(ptr , ist)
    if cnd is None :
        raise ValueError

    jd = JalaliDate(int(cnd.group(1)) , int(cnd.group(2)) , int(cnd.group(3)))
    date = jd.to_gregorian()

    t = time(int(cnd.group(5)) , int(cnd.group(6)) , int(cnd.group(7)))

    date_time = datetime.combine(date , t)
    return date_time

fu0 = make_datetime_from_iso_jdate_time
vect_make_datetime_from_iso_jdate_time = vectorize(fu0)

def find_jmonth_fr_df_col(df , targ_col , new_col , sep = '/') :
    s = df[targ_col].apply(convert_digits_to_en)

    pat = '(1[34]\d{2})' + sep + '(\d{2})' + sep + '\d{2}'
    _df = s.str.extract(pat)

    _df[new_col] = _df[0] + '-' + _df[1]

    df = df.join(_df[new_col])
    return df

def ex_all_jdate_fr_fa_str(s , sep = '/') :
    if not isinstance(s , str) :
        return s
    s = convert_digits_to_en(s)
    pat = '(1[34]\d{2})' + sep + '(\d{2})' + sep + '(\d{2})'
    return re.findall(pat , s)

def ex_1st_jdate_fr_fa_str(s , sep = '/') :
    ls = ex_all_jdate_fr_fa_str(s , sep)
    if isinstance(ls , list) and len(ls) > 0 :
        return ls[0]

def ex_1st_jmonth_fr_fa_str(s , sep = '/') :
    tu = ex_1st_jdate_fr_fa_str(s , sep)
    if isinstance(tu , tuple) :
        return tu[0] + '-' + tu[1]

def ret_an_iso_jdate_fr_a_date(date: str , date_fmt = '%Y-%m-%d') -> str :
    d = datetime.strptime(date , date_fmt)
    jd = JalaliDateTime.to_jalali(d)
    return jd.strftime('%Y-%m-%d')

def gen_jdate_fr_date_in_df(df , date_col , jdate_col , date_fmt = '%Y-%m-%d'
                            ) -> pd.DataFrame :
    d = date_col
    jd = jdate_col

    _df = df[[d]].drop_duplicates()
    _df['h'] = pd.to_datetime(_df[d] , format = date_fmt)

    fu = vectorize(JalaliDateTime.to_jalali)
    _df[jd] = _df['h'].apply(fu)

    _df = _df.drop(columns = 'h')

    df = df.merge(_df , on = d , how = 'left')

    return df

def gen_iso_jdate_fr_jdate_in_df(df , jdate_col , iso_jdate_col
                                 ) -> pd.DataFrame :
    jd = jdate_col
    ijd = 'h' if iso_jdate_col == jd else iso_jdate_col

    _df = df[[jd]].drop_duplicates()
    _df[ijd] = _df[jd].apply(lambda x : x.strftime('%Y-%m-%d'))

    df = df.merge(_df , on = jd , how = 'left')

    if ijd == 'h' :
        df = df.drop(columns = jd)
        df = df.rename(columns = {
                'h' : jd
                })

    return df
