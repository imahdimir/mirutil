"""

    """

import asyncio
from dataclasses import dataclass
from functools import partial

import nest_asyncio
from lxml.etree import XMLSyntaxError
from requests_html import AsyncHTMLSession

from .const import Const
from .files import write_txt_to_file_async


nest_asyncio.apply()

cte = Const()

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
