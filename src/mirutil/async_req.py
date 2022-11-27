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
                           client_session ,
                           headers = cte.headers ,
                           params = None ,
                           ssl = True ,
                           timeout = None) :
    try :
        r = await client_session.get(url ,
                                     headers = headers ,
                                     params = params ,
                                     ssl = ssl ,
                                     timeout = timeout)
        return RGet(r = r)
    except (ClientConnectorError , ClientPayloadError , ClientOSError) as e :
        print(e)
        return RGet(exc = str(e))

async def _process_rget(rget , mode , timeout) :
    if rget.exc is not None :
        return rget

    if rget.r.status != 200 :
        return rget

    if mode == 'read' :
        rget.cont = await rget.r.read(timeout = timeout)
    elif mode == 'json' :
        rget.cont = await rget.r.json(timeout = timeout)
    return rget

async def _get_resps_async(urls , mode , read_timeout , **kwargs) :
    sess = ClientSession()
    f = partial(_get_a_req_async , client_session = sess , **kwargs)
    co_tasks = [f(x) for x in urls]
    resps = await asyncio.gather(*co_tasks)
    f1 = partial(_process_rget , mode = mode , timeout = read_timeout)
    o = await asyncio.gather(*[f1(x) for x in resps])
    await sess.close()
    return o

def get_resps_async_sync(urls , mode = 'read' , read_timeout = 10 , **kwargs) :
    return asyncio.run(_get_resps_async(urls ,
                                        mode = mode ,
                                        read_timeout = read_timeout ,
                                        **kwargs))

async def _get_a_req_and_save_async(url ,
                                    fp ,
                                    client_session ,
                                    mode ,
                                    write_mode ,
                                    encoding ,
                                    get_timeout ,
                                    read_timeout ,
                                    **kwargs) :
    o = await _get_a_req_async(url ,
                               client_session ,
                               timeout = get_timeout ,
                               **kwargs)
    if o.r.status == 200 :
        o = await _process_rget(o , mode = mode , timeout = read_timeout)
        await write_to_file_async(o.cont , fp , write_mode , encoding)
    return o

async def _get_reqs_and_save_async(urls ,
                                   fps ,
                                   mode ,
                                   write_mode ,
                                   encoding ,
                                   get_timeout ,
                                   read_timeout ,
                                   **kwargs) :
    cs = ClientSession()
    f = partial(_get_a_req_and_save_async ,
                client_session = cs ,
                mode = mode ,
                write_mode = write_mode ,
                encoding = encoding ,
                get_timeout = get_timeout ,
                read_timeout = read_timeout ,
                **kwargs)
    co_tasks = [f(x , y) for x , y in zip(urls , fps)]
    o = await asyncio.gather(*co_tasks)
    await cs.close()
    return o

def get_reqs_and_save_async_sync(urls ,
                                 fps ,
                                 mode = 'read' ,
                                 write_mode = 'w' ,
                                 encoding = 'utf-8' ,
                                 get_timeout = 10 ,
                                 read_timeout = 10 ,
                                 **kwargs) :
    return asyncio.run(_get_reqs_and_save_async(urls ,
                                                fps ,
                                                mode = mode ,
                                                write_mode = write_mode ,
                                                encoding = encoding ,
                                                get_timeout = get_timeout ,
                                                read_timeout = read_timeout ,
                                                **kwargs))
