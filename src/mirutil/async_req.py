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

from .files import write_txt_to_file_async
from .const import Const


nest_asyncio.apply()

cte = Const()

@dataclass
class RGetReqAsync :
    status: int
    headers: dict
    cont: (bytes , None)

async def _get_req_async(url ,
                         headers = cte.headers ,
                         params = None ,
                         verify_ssl = True ,
                         timeout = None) :
    async with ClientSession() as s :
        try :
            r = await s.get(url ,
                            headers = headers ,
                            params = params ,
                            verify_ssl = verify_ssl ,
                            timeout = timeout)
            return RGetReqAsync(status = r.status ,
                                headers = r.headers ,
                                cont = await r.read())
        except ClientConnectorError as e :
            print(e)
            return RGetReqAsync(status = r.status ,
                                headers = r.headers ,
                                cont = None)

async def get_reqs_async(urls ,
                         headers = cte.headers ,
                         params = None ,
                         verify_ssl = True ,
                         timeout = None) :

    fu = partial(_get_req_async ,
                 headers = headers ,
                 params = params ,
                 verify_ssl = verify_ssl ,
                 timeout = timeout)
    co_tasks = [fu(x) for x in urls]
    return await asyncio.gather(*co_tasks)

async def get_texts_async(urls ,
                          headers = None ,
                          trust_env = False ,
                          params = None ,
                          verify_ssl = True ,
                          timeout = None) :

    fu = partial(get_reqs_async ,
                 headers = headers ,
                 params = params ,
                 trust_env = trust_env ,
                 verify_ssl = verify_ssl ,
                 timeout = timeout)

    return await fu(urls)

async def get_jsons_async(urls ,
                          content_type = None ,
                          headers = cte.headers ,
                          params = None ,
                          trust_env = False ,
                          verify_ssl = True ,
                          timeout = None , ) :

    fu = partial(get_reqs_async ,
                 headers = headers ,
                 params = params ,
                 trust_env = trust_env ,
                 verify_ssl = verify_ssl ,
                 timeout = timeout)

    rs = await fu(urls)

    return [await rs.json(content_type = content_type) for rs in rs]

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
    s = AsyncHTMLSession()
    r = await s.get(url ,
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
