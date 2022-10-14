"""

    """

import asyncio

import requests

from src.mirutil.async_requests import _get_req_async
from src.mirutil.async_requests import get_and_render_js_by_requests_html_async as grj


##
url = 'https://codal.ir/Reports/DownloadFile.aspx?id=lCbFkabC4qNOsjayDVl9nQ%3d%3d'

fu = _get_req_async(url)

r = asyncio.run(fu)

##

r = Res(status = 200 , cnt = 'a')
r

##
url = 'https://codal.ir/Reports/Decision.aspx?LetterSerial=RZQQQaQQQzaaQcLNBAkBMuVzTYXg%3D%3D&rt=0&let=58&ct=0&ft=-1'
fu = grj(url)
r = asyncio.run(fu)

##
r.status_code

##
