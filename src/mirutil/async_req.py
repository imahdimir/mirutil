"""

    """

import asyncio
from dataclasses import dataclass
from functools import partial

import nest_asyncio
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError
from aiohttp.client_exceptions import ClientPayloadError
from aiohttp.client_exceptions import ClientOSError

from .const import Const
from .files import write_to_file_async


nest_asyncio.apply()

cte = Const()

@dataclass
class RGetReqAsync :
    status: (int , None) = None
    headers: (dict , None) = None
    cont: (bytes , None) = None
    err: (str , None) = None

async def get_a_req_async(url ,
                          headers = cte.headers ,
                          params = None ,
                          ssl = True ,
                          timeout = None , ) :

    async with ClientSession() as s :

        try :
            r = await s.get(url ,
                            headers = headers ,
                            params = params ,
                            ssl = ssl ,
                            timeout = timeout , )

            return RGetReqAsync(status = r.status ,
                                headers = r.headers ,
                                cont = await r.read())

        except (ClientConnectorError , ClientPayloadError ,
                ClientOSError) as e :

            print(e)
            return RGetReqAsync(err = e)

async def get_reqs_async(urls , **kwargs) :
    fu = partial(get_a_req_async , **kwargs)
    co_tasks = [fu(x) for x in urls]
    return await asyncio.gather(*co_tasks)

def get_reqs_async_sync(urls , **kwargs) :
    return asyncio.run(get_reqs_async(urls , **kwargs))

async def get_a_req_and_save_async(url ,
                                   fp ,
                                   write_mode = 'w' ,
                                   encoding = 'utf-8' ,
                                   **kwargs) :
    fu = partial(get_a_req_async , **kwargs)
    o = await fu(url)
    if o.status == 200 :
        await write_to_file_async(o.cont , fp , write_mode , encoding)
    return o

async def get_reqs_and_save_async(urls , fps , **kwargs) :
    fu = partial(get_a_req_and_save_async , **kwargs)
    co_tasks = [fu(x , y) for x , y in zip(urls , fps)]
    return await asyncio.gather(*co_tasks)

def get_reqs_and_save_async_sync(urls , fps , **kwargs) :
    return asyncio.run(get_reqs_and_save_async(urls , fps , **kwargs))

async def get_jsons_async(urls , content_type = None , **kwargs) :
    fu = partial(get_a_req_async , **kwargs)
    rs = await fu(urls)
    return [await rs.json(content_type = content_type) for rs in rs]

def get_jsons_async_sync(urls , content_type = None , **kwargs) :
    return asyncio.run(get_jsons_async(urls , content_type , **kwargs))
