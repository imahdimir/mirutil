"""

    """

import asyncio

from src.mirutil.async_req import _get_a_req_async , ExClientResponse


##
url = 'https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=-1&Childs=true&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=-1&LetterType=-1&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber=1&Publisher=false&TracingNo=-1&search=false'
r = asyncio.run(_get_a_req_async(url))

##
r.status

##
ExClientResponse.from_client_response(r)

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
