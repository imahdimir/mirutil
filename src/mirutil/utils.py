"""

  """

import json
from pathlib import Path

from .df_utils import read_data_according_to_type
from .df_utils import save_df_as_a_nice_xl as sxl
from .namespaces import MetadataColumns


def get_tok_if_accessible(fp) :
    if Path(fp).exists() :
        with open(fp , 'r') as fi :
            return fi.read().strip()

def return_clusters_indices(iterable , cluster_size = 100) :
    intdiv = len(iterable) // cluster_size

    cis = [x * cluster_size for x in range(0 , intdiv + 1)]

    if len(cis) > 1 :
        if cis[-1] != len(iterable) :
            cis.append(cis[-1] + len(iterable) % cluster_size)
    else :
        cis = [0 , len(iterable)]
        if cis == [0 , 0] :
            cis = [0]

    cis[0] = cis[0]

    se_tuples = []
    for _i in range(len(cis) - 1) :
        si = cis[_i]
        ei = cis[_i + 1] - 1
        se = (si , ei)
        se_tuples.append(se)

    print(se_tuples)
    return se_tuples

def update_metadata_save_rand_sample(fp , save_rand_sample = True) :
    """
    :param fp:
    :param save_rand_sample:
    :return:
    """
    cns = MetadataColumns()

    dirpth = Path(fp).parent
    metafp = dirpth / 'META.json'
    if not metafp.exists() :
        return None

    with open(metafp) as fi :
        meta = json.load(fi)

    df = read_data_according_to_type(fp)

    if cns.startendcol in meta.keys() :
        if meta[cns.startendcol] is not None :
            meta[cns.start] = df[meta[cns.startendcol]].min()
            meta[cns.end] = df[meta[cns.startendcol]].max()

    meta[cns.numrow] = len(df)
    meta[cns.numcol] = len(df.columns)
    meta[cns.colnames] = list(df.columns)

    with open(metafp , 'w' , encoding = 'utf-8') as fi :
        json.dump(meta , fi , ensure_ascii = False)
        print("Meta updated.")

    if save_rand_sample and len(df) > 1000 :
        _df = df.sample(n = 1000)
        _fp = Path(fp).with_stem('Sample').with_suffix('.xlsx')
        sxl(_df , _fp)
        print('random sample saved.')