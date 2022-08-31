"""

  """
##
import re

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

##

##