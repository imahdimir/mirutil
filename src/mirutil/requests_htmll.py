"""

    """

import asyncio
from dataclasses import dataclass
from functools import partial

import nest_asyncio
from lxml.etree import XMLSyntaxError
from requests_html import HTMLSession
from requests_html import AsyncHTMLSession
from pyppeteer.errors import TimeoutError as tout
from pyppeteer.errors import PageError
from requests.exceptions import ConnectionError

from .const import Const
from .files import write_txt_to_file_async


nest_asyncio.apply()

cte = Const()

def download_chromium_if_not_installed() :
    """download chromium if not installed"""
    url = 'https://python.org'
    with HTMLSession() as s :
        r = s.get(url , headers = cte.headers)
    r.html.render(timeout = 30)

@dataclass
class RGetAndRender :
    status: int
    headers: dict
    html: (str , None)

async def get_and_render_by_requests_html_async(url ,
                                                headers = cte.headers ,
                                                params = None ,
                                                verify = True ,
                                                get_timeout = None ,
                                                render_timeout = None) :
    ret = RGetAndRender
    async with AsyncHTMLSession() as a :
        r = await a.get(url ,
                        headers = headers ,
                        params = params ,
                        verify = verify ,
                        timeout = get_timeout)
    try :
        await r.html.arender(timeout = render_timeout)
        return ret(status = r.status_code ,
                   headers = r.headers ,
                   html = r.html.html)
    except (XMLSyntaxError , tout , PageError , ConnectionError) as e :
        print(e)
        return ret(status = r.status_code , headers = r.headers , html = None)

async def get_a_rendered_html_and_save_async(url ,
                                             fp ,
                                             headers = cte.headers ,
                                             params = None ,
                                             verify = True ,
                                             get_timeout = None ,
                                             render_timeout = None) :
    fu = get_and_render_by_requests_html_async
    o = await fu(url ,
                 headers = headers ,
                 params = params ,
                 verify = verify ,
                 get_timeout = get_timeout ,
                 render_timeout = render_timeout)

    outer_html = o.html
    if outer_html :
        await write_txt_to_file_async(outer_html , fp)

    return o

async def get_rendered_htmls_and_save_async(urls ,
                                            fps ,
                                            headers = cte.headers ,
                                            params = None ,
                                            verify = True ,
                                            get_timeout = None ,
                                            render_timeout = None) :
    fu = partial(get_a_rendered_html_and_save_async ,
                 headers = headers ,
                 params = params ,
                 verify = verify ,
                 get_timeout = get_timeout ,
                 render_timeout = render_timeout)
    co_tasks = [fu(x , y) for x , y in zip(urls , fps)]
    return await asyncio.gather(*co_tasks)
