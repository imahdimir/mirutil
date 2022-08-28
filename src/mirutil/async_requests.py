##


import asyncio
from functools import partial

import nest_asyncio
from aiohttp import ClientSession


nest_asyncio.apply()


##
# getting resp text async funcs

async def get_a_resp_text_async(url , trust_env , params , verify_ssl) :
  async with ClientSession(trust_env = trust_env) as ses :
    async with ses.get(url ,
                       params = params ,
                       verify_ssl = verify_ssl) as resp :
      return await resp.text()


async def get_reps_texts_async(urls ,
                               trust_env = False ,
                               params = None ,
                               verify_ssl = True
                               ) :
  fu = partial(get_a_resp_text_async ,
               trust_env = trust_env ,
               params = params ,
               verify_ssl = verify_ssl)

  co_tasks = [fu(x) for x in urls]

  return await asyncio.gather(*co_tasks)


##
# getting resp json async funcs

async def get_a_resp_json_async(url ,
                                trust_env ,
                                params ,
                                verify_ssl ,
                                content_type
                                ) :
  async with ClientSession(trust_env = trust_env) as ses :
    async with ses.get(url ,
                       params = params ,
                       verify_ssl = verify_ssl) as resp :
      return await resp.json(content_type = content_type)


async def get_reps_jsons_async(urls ,
                               trust_env = False ,
                               params = None ,
                               verify_ssl = True ,
                               content_type = None
                               ) :
  fu = partial(get_a_resp_json_async ,
               trust_env = trust_env ,
               params = params ,
               verify_ssl = verify_ssl ,
               content_type = content_type)

  co_tasks = [fu(x) for x in urls]

  return await asyncio.gather(*co_tasks)