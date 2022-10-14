"""

    """

import asyncio
from dataclasses import dataclass
from functools import partial

import nest_asyncio
from aiohttp import ClientSession
from lxml.etree import XMLSyntaxError
from requests_html import AsyncHTMLSession
from pyppeteer.errors import TimeoutError
from aiohttp.client_exceptions import ClientConnectorError

from .utils import write_txt_to_file_async
from .const import Const


nest_asyncio.apply()

cte = Const()


@dataclass
class RGetReqAsync :
    status: int
    headers: dict
    cnt: (bytes , None)


async def _get_req_async(url ,
                         headers = cte.headers ,
                         params = None ,
                         trust_env = False ,
                         verify_ssl = True ,
                         timeout = None) :

    async with ClientSession(trust_env = trust_env) as s :

        try :
            r = await s.get(url ,
                            headers = headers ,
                            params = params ,
                            verify_ssl = verify_ssl ,
                            timeout = timeout)

            return RGetReqAsync(status = r.status ,
                                headers = r.headers ,
                                cnt = await r.read())

        except ClientConnectorError as e :
            print(e)
            return RGetReqAsync(status = r.status ,
                                headers = r.headers ,
                                cnt = None)


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


# getting resp cnt async funcs
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
                return await resp.cnt()


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

@dataclass
class RGetAndRender :
    status: int
    headers: dict
    html: (str , None)


async def get_and_render_js_by_requests_html_async(url ,
                                                   headers = cte.headers ,
                                                   params = None ,
                                                   verify = True ,
                                                   timeout = None) :
    ret = RGetAndRender

    ses = AsyncHTMLSession()

    r = await ses.get(url ,
                      headers = headers ,
                      params = params ,
                      verify = verify ,
                      timeout = timeout)

    try :
        await r.html.arender()
        return ret(status = r.status_code ,
                   headers = r.headers ,
                   html = r.html.html)

    except (XMLSyntaxError , TimeoutError) as e :
        print(e)
        return ret(status = r.status_code , headers = r.headers , html = None)


async def get_a_rendered_html_and_save_async(url ,
                                             fp ,
                                             headers = cte.headers ,
                                             params = None ,
                                             verify = True ,
                                             timeout = None) :
    fu = get_and_render_js_by_requests_html_async
    ou = await fu(url ,
                  headers = headers ,
                  params = params ,
                  verify = verify ,
                  timeout = timeout)

    outer_html = ou.html
    if outer_html :
        await write_txt_to_file_async(outer_html , fp)


async def get_rendered_htmls_and_save_async(urls ,
                                            fps ,
                                            headers = cte.headers ,
                                            params = None ,
                                            verify = True ,
                                            timeout = None) :
    fu = partial(get_a_rendered_html_and_save_async ,
                 headers = headers ,
                 params = params ,
                 verify = verify ,
                 timeout = timeout)

    co_tasks = [fu(x , y) for x , y in zip(urls , fps)]
    return await asyncio.gather(*co_tasks)
