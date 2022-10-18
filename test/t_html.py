"""

    """

import importlib

import pandas as pd

from src.mirutil import html


importlib.reload(html)

from src.mirutil.html import *


##
def read_html(fp) -> str :
    with open(fp , 'r') as f :
        return f.read()

fp = '/Users/mahdi/Dropbox/1-git-dirs/PyCharm/u-d0-FirmTicker-MonthlySales/rd-Codal-monthly-sales-htmls/741620.html'

ht = read_html(fp)

tr = parse_html_as_etree(ht)
##
fu = rm_hidden_elements_of_etree
tr1 = fu(tr)

html = etree_to_html(tr1)

##
from html_table_parser import HTMLTableParser


p = HTMLTableParser()
p.feed(html)

dfs = [pd.DataFrame(x) for x in p.tables]
df = pd.concat(dfs)

##
