"""

    """

import asyncio
from dataclasses import dataclass
from functools import partial

import nest_asyncio
from lxml.etree import XMLSyntaxError
from pyppeteer.errors import PageError
from pyppeteer.errors import TimeoutError as tout
from requests.exceptions import ConnectionError
from requests_html import AsyncHTMLSession
from requests_html import HTMLSession

from .const import Const
from .files import write_txt_to_file
from .files import write_txt_to_file_async


nest_asyncio.apply()

cte = Const()

def download_chromium_if_not_installed() :
    """download chromium if not installed"""
    url = 'https://google.com'

    s = HTMLSession()
    r = s.get(url , headers = cte.headers , timeout = 10)
    s.close()

    r.html.render(timeout = 30)

@dataclass
class RGetAndRender :
    status: int
    headers: dict
    html: (str , None) = None
    err: (str , None) = None

async def get_and_render_by_requests_html_async(url ,
                                                headers = cte.headers ,
                                                params = None ,
                                                verify = True ,
                                                get_timeout = None ,
                                                render_timeout = None) :
    a = AsyncHTMLSession()
    await a.close()

    r = await a.get(url ,
                    headers = headers ,
                    params = params ,
                    verify = verify ,
                    timeout = get_timeout)

    await a.close()

    try :
        await r.html.arender(timeout = render_timeout)
        return RGetAndRender(status = r.status_code ,
                             headers = r.headers ,
                             html = r.html.html ,
                             err = None)
    except (XMLSyntaxError , tout , PageError , ConnectionError) as e :
        print(e)
        return RGetAndRender(status = r.status_code ,
                             headers = r.headers ,
                             html = None ,
                             err = e)

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

def get_and_render_by_requests_html(url ,
                                    headers = cte.headers ,
                                    params = None ,
                                    verify = True ,
                                    get_timeout = None ,
                                    render_timeout = None) :
    """ makes a get request & renders it javascript """

    hs = HTMLSession()
    r = hs.get(url ,
               headers = headers ,
               params = params ,
               verify = verify ,
               timeout = get_timeout)
    hs.close()

    try :
        r.html.render(timeout = render_timeout)
        return RGetAndRender(status = r.status_code ,
                             headers = r.headers ,
                             html = r.html.html ,
                             err = None)

    except (XMLSyntaxError , tout , PageError , ConnectionError) as e :
        print(e)
        return RGetAndRender(status = r.status_code ,
                             headers = r.headers ,
                             html = None ,
                             err = e)

def get_a_rendered_html_and_save(url ,
                                 fp ,
                                 headers = cte.headers ,
                                 params = None ,
                                 verify = True ,
                                 get_timeout = None ,
                                 render_timeout = None) :
    o = get_and_render_by_requests_html(url ,
                                        headers = headers ,
                                        params = params ,
                                        verify = verify ,
                                        get_timeout = get_timeout ,
                                        render_timeout = render_timeout)
    outer_html = o.html
    if outer_html :
        write_txt_to_file(outer_html , fp)
    return o
