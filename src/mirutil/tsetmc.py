"""

  """

import re
from functools import partial

import pandas as pd
import requests

from .async_requests import get_reps_texts_async


headers = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }
skey = 'srchkey'

async def search_tsetmc_async(string_list) :
    urls = [make_tsetmc_srch_url(x) for x in string_list]

    fu = partial(get_reps_texts_async ,
                 trust_env = False ,
                 params = None ,
                 verify_ssl = True)

    resps = await fu(urls)

    df = pd.DataFrame()

    for ist , res in zip(string_list , resps) :
        _df = make_a_df_from_a_resp_text_tsetmc(res)
        _df[skey] = ist

        df = pd.concat([df , _df])

    return df

def search_tsetmc_ret_df(string) :
    url = make_tsetmc_srch_url(string)

    rsp = requests.get(url , headers = headers)
    rtxt = rsp.text

    df = make_a_df_from_a_resp_text_tsetmc(rtxt)
    df[skey] = string
    return df

def make_tsetmc_srch_url(istr) :
    return f'http://www.tsetmc.com/tsev2/data/search.aspx?skey={istr}'

def make_a_df_from_a_resp_text_tsetmc(rsp) :
    order_map = {
            'Ticker'   : 0 ,
            'Name'     : 1 ,
            'ID-1'     : 2 ,
            'ID-2'     : 3 ,
            'ID-3'     : 4 ,
            'ID-4'     : 5 ,
            'unk6'     : 6 ,
            'IsActive' : 7 ,
            'unk8'     : 8 ,
            'unk9'     : 9 ,
            'Market'   : 10 ,
            }

    rows = rsp.split(';')
    rows = [x for x in rows if x != '']

    df = pd.DataFrame(columns = order_map.keys())

    for rw in rows :
        vals = rw.split(',')
        dfr = order_map.copy()

        for ky , vl in order_map.items() :
            try :
                dfr[ky] = vals[vl]
            except IndexError :
                dfr[ky] = None

        _df = pd.DataFrame(data = dfr , index = [0])
        df = pd.concat([df , _df] , ignore_index = True)
    return df

def extract_market_from_tsetmc_title(title: str) :
    os = title.replace("',FaraDesc ='" , ' ')
    os = os.strip()

    ptr = r'.+-\s*([^-]*)'
    if re.fullmatch(ptr , os) :
        return re.sub(ptr , r'\1' , os).strip()
    else :
        ptr = r'.+-\s*-\s*'
        assert re.fullmatch(ptr , os)

def make_tsetmc_overview_pg_url_with_testmc_id(tsetmc_id) :
    return f'http://www.tsetmc.com/Loader.aspx?ParTree=151311&i={tsetmc_id}'

def get_an_id_testmc_overview_page_resp(tsetmc_id) :
    url = make_tsetmc_overview_pg_url_with_testmc_id(tsetmc_id)
    return requests.get(url , headers = headers)

def get_title_fr_resp_text(resp_text) :
    return re.findall(r"Title='(.+)',FaraDesc" , resp_text)

def get_group_name_fr_resp_text(resp_text) :
    return re.findall(r"LSecVal='(.+)',CgrValCot" , resp_text)

def get_title_from_overview_page_by_stock_id(tsetmc_id) :
    resp = get_an_id_testmc_overview_page_resp(tsetmc_id)
    return get_title_fr_resp_text(resp.text)

def get_groupname_from_overview_page_by_stock_id(tsetmc_id) :
    resp = get_an_id_testmc_overview_page_resp(tsetmc_id)
    return get_group_name_fr_resp_text(resp.text)
