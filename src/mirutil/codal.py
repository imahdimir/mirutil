"""

    """

import re
from dataclasses import dataclass


@dataclass
class RFindFn :
    fn: (str , None)
    suf: (str , None)


def find_fn_and_suf_fr_codal_get_resp(r_header) :
    cd = r_header["Content-Disposition"]

    pat = 'filename=(.+)\.(\w+)'
    rf = re.findall(pat , cd)
    if len(rf) == 0 :
        return RFindFn(None , None)

    g = rf[0]

    return RFindFn(fn = g[0] , suf = g[1])
