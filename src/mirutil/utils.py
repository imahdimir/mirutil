"""

  """

def ret_clusters_indices(iterable , cluster_size = 100) :
    """ clusters the iterable into clusters of size cluster_size
        and returns the start and end indices of each cluster
        in a list of tuples of start and end indices

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

    se_tuples = []
    for _i in range(len(cis) - 1) :
        se = (cis[_i] , cis[_i + 1])
        se_tuples.append(se)

    prt = se_tuples[0 :3]
    _ = [print(x) for x in prt]

    print('..')

    prt = se_tuples[-2 :]
    _ = [print(x) for x in prt]
    return se_tuples

def print_list_as_dict_fmt(lst) :
    """ prints the list as a dictionary format with the elements as keys"""
    for item in lst :
        print('"' + item + '" : None ,')

async def write_txt_to_file_async(txt , fp) :
    with open(fp , "w") as file :
        file.write(txt)
