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
from requests.exceptions import ReadTimeout as rtout
from requests_html import AsyncHTMLSession
from requests_html import HTMLSession

from .const import Const
from .files import write_txt_to_file_async


nest_asyncio.apply()

cte = Const()
ases = AsyncHTMLSession()

def download_chromium_if_not_installed(url = 'https://www.google.com') :
    """ downloads chromium if it is not installed """
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

async def get_a_req_and_render_by_requests_html_async(url ,
                                                      headers = cte.headers ,
                                                      params = None ,
                                                      verify = True ,
                                                      get_timeout = None ,
                                                      render_timeout = None) :
    r = await ases.get(url ,
                       headers = headers ,
                       params = params ,
                       verify = verify ,
                       timeout = get_timeout)
    try :
        await r.html.arender(timeout = render_timeout)
        return RGetAndRender(status = r.status_code ,
                             headers = r.headers ,
                             html = r.html.html ,
                             err = None)
    except (XMLSyntaxError , tout , PageError , ConnectionError , rtout) as e :
        print(e)
        return RGetAndRender(status = r.status_code ,
                             headers = r.headers ,
                             html = None ,
                             err = e)

def get_a_req_and_render_by_requests_html(url , **kwargs) :
    fu = get_a_req_and_render_by_requests_html_async(url , **kwargs)
    return asyncio.run(fu)

async def get_a_rendered_html_and_save_async(url , fp , **kwargs) :
    fu = partial(get_a_req_and_render_by_requests_html_async , **kwargs)
    o = await fu(url)
    outer_html = o.html
    if outer_html :
        await write_txt_to_file_async(outer_html , fp)
    return o

async def get_rendered_htmls_and_save_async(urls , fps , **kwargs) :
    fu = partial(get_a_rendered_html_and_save_async , **kwargs)
    co_tasks = [fu(x , y) for x , y in zip(urls , fps)]
    return await asyncio.gather(*co_tasks)

def get_rendered_htmls_and_save_async_sync(urls , fps , **kwargs) :
    return asyncio.run(get_rendered_htmls_and_save_async(urls , fps , **kwargs))
