"""

    """

import asyncio

import requests

from src.mirutil.async_requests import Res
from src.mirutil.async_requests import _get_req_async


##
url = 'https://codal.ir/Reports/DownloadFile.aspx?id=lCbFkabC4qNOsjayDVl9nQ%3d%3d'

fu = _get_req_async(url)

r = asyncio.run(fu)

##

r = Res(status = 200 , cnt = 'a')
r
