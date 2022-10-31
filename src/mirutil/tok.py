"""

    """

from dataclasses import dataclass
from pathlib import Path

import requests

from .files import read_json_file as rjf


@dataclass
class KeyVal :
    key: str
    val: str

def get_local_toks_js_fp(raw_github_url = 'https://raw.github.com/imahdimir/tok/main/fps.json') :
    rsp = requests.get(raw_github_url)
    js = rsp.json()
    for fp in js.values() :
        if Path(fp).exists() :
            return fp

def get_val_by_key_fr_json(fp , key = None) :
    js = rjf(fp)
    if key is None :
        return KeyVal(key = list(js.keys())[0] , val = list(js.values())[0])
    return KeyVal(key = key , val = js[key])

def get_token(key = None) :
    fp = get_local_toks_js_fp()
    if fp is not None :
        o = get_val_by_key_fr_json(fp , key = key)
        return o.val
    tok = input('Enter token: ')
    return tok
