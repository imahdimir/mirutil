"""

    """

import asyncio
from functools import partial

import nest_asyncio
from aiohttp import ClientSession
from lxml.etree import XMLSyntaxError
from requests_html import AsyncHTMLSession
from pyppeteer.errors import TimeoutError
from aiohttp.client_exceptions import ClientConnectorError

from .utils import write_txt_to_file_async
from .const import Const


ases = AsyncHTMLSession()

nest_asyncio.apply()

cte = Const()


async def _get_req_async(url ,
                         headers = cte.headers ,
                         params = None ,
                         trust_env = False ,
                         verify_ssl = True ,
                         timeout = None) :

    async with ClientSession(trust_env = trust_env) as s :
        try :
            return await s.get(url ,
                               headers = headers ,
                               params = params ,
                               verify_ssl = verify_ssl ,
                               timeout = timeout)
        except ClientConnectorError as e :
            print(e)
            return e


async def get_reqs_async(urls ,
                         headers = cte.headers ,
                         params = None ,
                         trust_env = False ,
                         verify_ssl = True ,
                         timeout = None) :

    fu = partial(_get_req_async ,
                 headers = headers ,
                 params = params ,
                 trust_env = trust_env ,
                 verify_ssl = verify_ssl ,
                 timeout = timeout)

    co_tasks = [fu(x) for x in urls]
    return await asyncio.gather(*co_tasks)


# getting resp text async funcs
async def get_a_resp_text_async(url ,
                                headers ,
                                trust_env ,
                                params ,
                                verify_ssl ,
                                timeout) :
    async with ClientSession(trust_env = trust_env) as ses :
        async with ses.get(url ,
                           params = params ,
                           headers = headers ,
                           verify_ssl = verify_ssl ,
                           timeout = timeout) as resp :
            if resp.status == 200 :
                return await resp.text()


async def get_reps_texts_async(urls ,
                               headers = None ,
                               trust_env = False ,
                               params = None ,
                               verify_ssl = True ,
                               timeout = None) :
    fu = partial(get_a_resp_text_async ,
                 headers = headers ,
                 trust_env = trust_env ,
                 params = params ,
                 verify_ssl = verify_ssl ,
                 timeout = timeout)
    co_tasks = [fu(x) for x in urls]
    return await asyncio.gather(*co_tasks)


# getting resp json async funcs
async def get_a_resp_json_async(url ,
                                headers ,
                                trust_env ,
                                params ,
                                verify_ssl ,
                                content_type) :
    async with ClientSession(trust_env = trust_env) as ses :
        async with ses.get(url ,
                           headers = headers ,
                           params = params ,
                           verify_ssl = verify_ssl) as resp :
            if resp.status == 200 :
                return await resp.json(content_type = content_type)


async def get_reps_jsons_async(urls ,
                               headers = None ,
                               trust_env = False ,
                               params = None ,
                               verify_ssl = True ,
                               content_type = None) :
    fu = partial(get_a_resp_json_async ,
                 headers = headers ,
                 trust_env = trust_env ,
                 params = params ,
                 verify_ssl = verify_ssl ,
                 content_type = content_type)

    co_tasks = [fu(x) for x in urls]

    return await asyncio.gather(*co_tasks)


# getting & saving rendered Htmls async funcs
async def render_js_async(url) :
    r = await ases.get(url , verify = False)
    try :
        await r.html.arender()
        return r.html.html
    except (XMLSyntaxError , TimeoutError) as e :
        print(e)
        return


async def get_a_rendered_html_and_save(url , fp) :
    txt = await render_js_async(url)
    if txt :
        await write_txt_to_file_async(txt , fp)


async def get_rendered_htmls_and_save(urls , fps) :
    fu = get_a_rendered_html_and_save
    co_tasks = [fu(x , y) for x , y in zip(urls , fps)]
    return await asyncio.gather(*co_tasks)
