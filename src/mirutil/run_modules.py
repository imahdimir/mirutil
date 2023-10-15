"""

    """

import runpy
import shutil
from pathlib import Path

from .dirr import DefaultDirs

def get_modules_to_run_from_path(modules_dir: Path | str) -> list[Path] :
    """
    finds all .py files in modules_dir that start with '_' and
    sorts them based on the number after '_'. This is the convention
    I use to specify modules to run in order. The number after '_' is
    used to specify the order. There might be other modules in the same
    dir that are not prefixed with '_' and they will not be run. There
    are auxiliary modules.
    """

    # get all .py files in modules_dir
    pys = Path(modules_dir).glob('*.py')

    # filter those that start with '_'
    ms = [x for x in pys if x.name.startswith('_')]

    # sort .py files them based on the number after _
    ms = sorted(ms)

    return ms

def run_modules_from_dir_in_order(modules_dir: Path | str = DefaultDirs().m) -> None :
    """
    runs all modules in modules_dir that start with '_' based on the number
    after '_'.
    """
    ms = get_modules_to_run_from_path(modules_dir)
    # run modules in order
    for m in ms :
        print('\n\t*** Running them module : {}  ***\n'.format(m.name))

        runpy.run_path(str(m) , run_name = '__main__')

        print('\n\t*** The Module {} Done! ***\n'.format(m.name))

def clean_cache_dirs(inculding_set: set[Path] = None ,
                     excluding_set: set[Path] = None ,
                     inculde_defaults: bool = True
                     ) -> None :
    """
    removes cache dirs
    some defaults + some manual to include - some to exculde

    include_defaults: whether to include defaults
    """

    # default argument values
    if excluding_set is None :
        excluding_set = {}
    if inculding_set is None :
        inculding_set = {}

    # default dirs
    if inculde_defaults :
        dyr = DefaultDirs()
        dyrs = {dyr.gd , dyr.t}
    else :
        dyrs = {}

    # include & exclude manually
    dyrs = dyrs.union(inculding_set)
    dyrs = dyrs.difference(excluding_set)

    # remove the final set of dirs one by one
    print('Cleaning cache directories : ' , dyrs)

    for di in dyrs :
        shutil.rmtree(di , ignore_errors = True)

    print('All cache dirs got removed.')
