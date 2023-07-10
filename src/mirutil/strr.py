"""

  """

import re
import pandas as pd

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
            '\u202b' : ' ' ,
            '\u200c' : ' ' ,
            '\u200d' : '' ,
            '\u200f' : '' ,
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

def normalize_fa_str_completely(fa_str: str) -> str :
    if not isinstance(fa_str , str) :
        return fa_str
    os = convert_digits_to_en(fa_str)
    os = characters.ar_to_fa(os)
    os = rm_odd_chars(os)
    os = strip_and_rm_successive_spaces(os)
    return os

def normalize_completley_and_rm_all_whitespaces(fa_str: str) -> str :
    if not isinstance(fa_str , str) :
        return fa_str
    os = normalize_fa_str_completely(fa_str)
    _2rep = {
            '\n'   : None ,
            '\t'   : None ,
            '\r\n' : None ,
            ','    : None ,
            ' '    : None ,
            }
    for k in _2rep.keys() :
        os = os.replace(k , '')
    return os

def any_of_patterns_matches(istr , patterns) :
    if not isinstance(istr , str) :
        return istr

    for pattern in patterns :
        if re.fullmatch(pattern , istr) :
            return True

    return False
