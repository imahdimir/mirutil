"""

    """

import runpy
import shutil
from pathlib import Path

from .dirr import DefaultDirs

def get_modules_to_run_from_path(modules_dir: Path | str) -> list[Path] :
    """

    """

    # get all .py files in modules_dir
    pys = Path(modules_dir).glob('*.py')

    # filter those that start with '_'
    moduls = [x for x in pys if x.name.startswith('_')]

    # sort them based on the number after _
    moduls = sorted(moduls)

    return moduls

def run_modules_from_dir_in_order(modules_dir: Path | str) -> None :
    """

    """

    ms = get_modules_to_run_from_path(modules_dir)

    # run modules in order
    for m in ms :
        print('Running : ' , m.name)

        runpy.run_path(str(m) , run_name = '__main__')

def clean_cache_dirs(inculding_set: set[Path] = None ,
                     excluding_set: set[Path] = None ,
                     inculde_defaults: bool = True
                     ) -> None :
    """
    removes cache dirs
    some defaults + some manual to include - some to exculde

    : include_defaults: whether to include defaults
    """

    # default argument values
    if excluding_set is None :
        excluding_set = {}
    if inculding_set is None :
        inculding_set = {}

    # default dirs
    if inculde_defaults :
        dyr = DefaultDirs()
        dyrs = {dyr.gd , dyr.td}
    else :
        dyrs = {}

    # include & exclude manually
    dyrs = dyrs.union(set(inculding_set))
    dyrs = dyrs.difference(set(excluding_set))

    # remove final set of dirs one by one
    print('Cleaning cache : ' , dyrs)

    for di in dyrs :
        shutil.rmtree(di , ignore_errors = True)

    print('All cache dirs got removed.')
