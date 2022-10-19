"""

    """

from pathlib import Path

import openpyxl as pyxl
import pandas as pd
from itertools import product


def save_df_as_a_nice_xl(df ,
                         fpn ,
                         index: bool = False ,
                         header: bool = True ,
                         max_col_length: int = 40) -> None :
    df.to_excel(fpn , index = False)

    wb = pyxl.load_workbook(fpn)
    ws = wb.active

    panes = index * ws['A'] + header * ws[1]

    for cell in panes :
        cell.style = 'Pandas'

    for column in ws.columns :
        length = max(len(str(cell.value)) for cell in column) + 3
        length = length if length <= max_col_length else max_col_length
        ws.column_dimensions[column[0].column_letter].width = length

    ws.freeze_panes = 'A2'

    wb.save(fpn)
    wb.close()
    print(f"saved as {fpn}")

def save_as_prq_wo_index(df , fpn) -> None :
    df.to_parquet(fpn , index = False)
    print(f'dataframe saved as {fpn} without index')

def read_data_according_to_type(fpn) -> pd.DataFrame :
    suf = Path(fpn).suffix
    if suf == '.xlsx' :
        return pd.read_excel(fpn)
    elif suf == '.prq' :
        return pd.read_parquet(fpn)
    elif suf == '.csv' :
        return pd.read_csv(fpn)

def has_extra_data(df , df1) -> bool :
    df = df.convert_dtypes()
    df1 = df1.convert_dtypes()

    df = df.astype('string')
    df1 = df1.astype('string')

    _df = pd.concat([df , df1])

    _df = _df.drop_duplicates()

    return not df.equals(_df)

def drop_dup_and_sub_dfs(dfs_list: list) -> list :
    """

    assumption: len(dfs_list) >= 2
    """

    dfs1 = [(i , df) for i , df in enumerate(dfs_list)]

    pr = product(dfs_list , dfs1)
    pr = list(pr)

    df = pd.DataFrame(pr , columns = [0 , 1])

    df[2] = df[1].apply(lambda x : x[0])
    df[1] = df[1].apply(lambda x : x[1])

    ms = df.apply(lambda x : x[0].equals(x[1]) , axis = 1)
    df = df[~ ms]

    df[3] = df.apply(lambda x : has_extra_data(x[0] , x[1]) , axis = 1)

    df[4] = df.groupby(2)[3].transform('all')

    ms = df[4]
    df = df[ms]

    df = df.drop_duplicates(subset = 2)

    return df[1].to_list()

def find_all_df_locs_eq_val(df: pd.DataFrame , val) -> pd.MultiIndex :
    msk = df.eq(val)
    _df = df[msk]
    s = _df.stack()
    return s.index

def ret_north_west_of_multiindex(mi: pd.MultiIndex) :
    df = mi.to_frame()
    if df.empty :
        return
    df = df.sort_values(by = [0 , 1] , ascending = False)
    r = df.iloc[0]
    return r.index
