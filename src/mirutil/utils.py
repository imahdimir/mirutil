"""

  """

def ret_clusters_indices(iterable , cluster_size = 100) :
    """ clusters the iterable into clusters of size cluster_size
        and returns the start and end indices of each cluster
        in a list of tuples

    :param iterable: the iterable to be clustered
    :param cluster_size: the size of each cluster
    :return: list of tuples of start and end indices of each cluster
    """
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

    prt = se_tuples[0 :3] + se_tuples[-2 :]
    for el in prt :
        print(el)
    return se_tuples

def list_all_files_recursively_in_all_subdirs(root_dir) :
    """ lists all files in all subdirectories of the root_dir

    :param root_dir: the root to start the search from
    :return: list of pathes to all files in all subdirectories of the root_dir
    """
    import os

    all_files = []
    for root , dirs , files in os.walk(root_dir) :
        for file in files :
            all_files.append(os.path.join(root , file))
    return all_files

def print_list_as_dict_fmt(lst) :
    """ prints the list as a dictionary format with the elements as keys"""
    for item in lst :
        print('"' + item + '" : None ,')
