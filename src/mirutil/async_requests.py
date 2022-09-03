"""

    """

import asyncio
from functools import partial

import nest_asyncio
from aiohttp import ClientSession


nest_asyncio.apply()

# getting resp text async funcs
async def get_a_resp_text_async(url ,
                                trust_env ,
                                params ,
                                headers ,
                                verify_ssl ,
                                timeout) :
    async with ClientSession(trust_env = trust_env) as ses :
        async with ses.get(url ,
                           params = params ,
                           headers = headers ,
                           verify_ssl = verify_ssl ,
                           timeout = timeout) as resp :
            if resp.status == 200 :
                return await resp.text()

async def get_reps_texts_async(urls ,
                               trust_env = False ,
                               params = None ,
                               headers = None ,
                               verify_ssl = True ,
                               timeout = None) :
    fu = partial(get_a_resp_text_async ,
                 trust_env = trust_env ,
                 params = params ,
                 headers = headers ,
                 verify_ssl = verify_ssl ,
                 timeout = timeout)
    co_tasks = [fu(x) for x in urls]
    return await asyncio.gather(*co_tasks)

# getting resp json async funcs

async def get_a_resp_json_async(url ,
                                trust_env ,
                                params ,
                                verify_ssl ,
                                content_type) :
    async with ClientSession(trust_env = trust_env) as ses :
        async with ses.get(url ,
                           params = params ,
                           verify_ssl = verify_ssl) as resp :
            if resp.status == 200 :
                return await resp.json(content_type = content_type)

async def get_reps_jsons_async(urls ,
                               trust_env = False ,
                               params = None ,
                               verify_ssl = True ,
                               content_type = None) :
    fu = partial(get_a_resp_json_async ,
                 trust_env = trust_env ,
                 params = params ,
                 verify_ssl = verify_ssl ,
                 content_type = content_type)

    co_tasks = [fu(x) for x in urls]

    return await asyncio.gather(*co_tasks)