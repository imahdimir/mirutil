"""

    """

import re


def find_fn_and_suf_fr_codal_get_resp(r) :
    hdr = r.headers
    cd = hdr["Content-Disposition"]

    pat = 'filename=(.+)\.(\w+)'
    rf = re.findall(pat , cd)
    g0 = rf[0]
    fn , suf = g0
    return {
            "fn"  : fn ,
            "suf" : suf
            }
