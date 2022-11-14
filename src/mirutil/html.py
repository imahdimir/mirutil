"""

    """

import pandas as pd
from html_table_parser.parser import HTMLTableParser
from lxml import etree


hdn_xpth = {
        "//*[@hidden]"                          : None ,
        '//*[contains(@style, "display:none")]' : None ,
        '//*[@class="non-visible-first"]'       : None ,
        }

def make_hidden_elements_of_etree_row_col_span_zero(tree: etree) -> etree :
    for xp in hdn_xpth.keys() :
        for el in tree.xpath(xp) :
            el.set("rowspan" , "0")
            el.set("colspan" , "0")
    return tree

def rm_hidden_elements_of_etree(tree: etree) -> etree :
    for xp in hdn_xpth.keys() :
        for el in tree.xpath(xp) :
            el.getparent().remove(el)

    return tree

def parse_html_as_etree(html: str) -> etree :
    parser = etree.HTMLParser()
    tree = etree.fromstring(html , parser)
    return tree

def etree_to_html(tree: etree) -> str :
    return etree.tostring(tree , encoding = "unicode" , method = "html")

def read_tables_in_html_by_html_table_parser(html: str) -> list :
    p = HTMLTableParser()
    p.feed(html)
    dfs = [pd.DataFrame(x) for x in p.tables]
    return dfs
