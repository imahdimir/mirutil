"""

    """

import requests

from src.mirutil.const import Const


cte = Const()

##
url = 'https://codal.ir/Reports/DownloadFile.aspx?id=lCbFkabC4qNOsjayDVl9nQ%3d%3d'
r = requests.get(url , headers = cte.headers)
r.status_code

##
r.content
