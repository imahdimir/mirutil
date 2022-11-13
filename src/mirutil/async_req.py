"""

    """

import asyncio
from dataclasses import dataclass
from functools import partial

import nest_asyncio
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError
from aiohttp.client_exceptions import ClientOSError
from aiohttp.client_exceptions import ClientPayloadError
from aiohttp import ClientResponse

from .const import Const
from .files import write_to_file_async


nest_asyncio.apply()

cte = Const()

@dataclass
class RGet :
    r: ClientResponse | None = None
    exc: str | None = None
    cont: bytes | None = None

async def _get_a_req_async(url ,
                           headers = cte.headers ,
                           params = None ,
                           ssl = True ,
                           timeout = None) :
    async with ClientSession() as s :
        try :
            r = await s.get(url ,
                            headers = headers ,
                            params = params ,
                            ssl = ssl ,
                            timeout = timeout)
            return RGet(r = r)
        except (
        ClientConnectorError , ClientPayloadError , ClientOSError) as e :
            print(e)
            return RGet(exc = str(e))

async def _process_rget(rget , mode) :
    if rget.exc is not None :
        return rget

    if rget.r.status != 200 :
        return rget

    if mode == 'read' :
        rget.cont = await rget.read()
    elif mode == 'json' :
        rget.cont = await rget.json()
    return rget

async def _get_resps_async(urls , mode , **kwargs) :
    f = partial(_get_a_req_async , **kwargs)
    co_tasks = [f(x) for x in urls]
    resps = await asyncio.gather(*co_tasks)
    return await asyncio.gather(*[_process_rget(x , mode) for x in resps])

def get_resps_async_sync(urls , mode = 'read' , **kwargs) :
    return asyncio.run(_get_resps_async(urls , mode = mode , **kwargs))

async def _get_a_req_and_save_async(url ,
                                    fp ,
                                    write_mode = 'w' ,
                                    encoding = 'utf-8' ,
                                    **kwargs) :
    fu = partial(_get_a_req_async , **kwargs)
    o = await fu(url)
    if o.status == 200 :
        o = await _process_rget(o , mode = 'read')
        await write_to_file_async(o.cont , fp , write_mode , encoding)
    return o

async def _get_reqs_and_save_async(urls , fps , **kwargs) :
    f = partial(_get_a_req_and_save_async , **kwargs)
    co_tasks = [f(x , y) for x , y in zip(urls , fps)]
    return await asyncio.gather(*co_tasks)

def get_reqs_and_save_async_sync(urls , fps , **kwargs) :
    return asyncio.run(_get_reqs_and_save_async(urls , fps , **kwargs))
