"""

    """

from pathlib import Path


def get_all_subdirs(root_dir) :
    """ returns all subdirectories of the root_dir"""
    return Path(root_dir).glob('**')

def list_all_files_recursively_in_all_subdirs(root_dir) :
    """ lists all files in all subdirectories of the root_dir

    :param root_dir: the root to start the search from
    :return: list of pathes to all files in all subdirectories of the root_dir
    """
    all_subdirs = get_all_subdirs(root_dir)
    all_files = []
    for d in all_subdirs :
        all_files.extend(list(d.glob('*')))
    return all_files

def has_subdir(dirp: Path) :
    for el in dirp.iterdir() :
        if el.is_dir() :
            return True
    return False
