"""

  """

from pathlib import Path


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

def list_all_files_recursively(root_dir) :
    """
    :param root_dir:
    :return:
    """
    import os

    all_files = []
    for root , dirs , files in os.walk(root_dir) :
        for file in files :
            all_files.append(os.path.join(root , file))

    return all_files

def print_list_as_dict_fmt(lst) :
    for item in lst :
        print('"' + item + '":None,')
