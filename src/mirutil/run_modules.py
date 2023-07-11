"""

    """

import runpy
from pathlib import Path

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
