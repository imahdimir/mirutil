"""

  """

import re

from persiantools import characters
from persiantools import digits


def convert_digits_to_en(istr) :
    if not isinstance(istr , str) :
        return istr
    os = digits.ar_to_fa(istr)
    os = digits.fa_to_en(os)
    return os

def rm_odd_chars(istr) :
    if not isinstance(istr , str) :
        return istr
    repmap = {
            r"\u202b" : ' ' ,
            r'\u200c' : ' ' ,
            r'\u200d' : '' ,
            r'\u200f' : '' ,
            }
    os = istr
    for ky , vl in repmap.items() :
        os = os.replace(ky , vl)
    return os

def strip_and_rm_successive_spaces(istr) :
    if not isinstance(istr , str) :
        return istr
    os = re.sub('\s+' , ' ' , istr)
    os = os.strip()
    return os

def normalize_fa_str_completely(fa_string) :
    if not isinstance(fa_string , str) :
        return fa_string
    os = convert_digits_to_en(fa_string)
    os = characters.ar_to_fa(os)
    os = rm_odd_chars(os)
    os = strip_and_rm_successive_spaces(os)
    return os
