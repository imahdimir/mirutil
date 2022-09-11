"""

    """

import shutil
from pathlib import Path


def rm_all_in_datalore_cwd() :
    """Remove all files and directories in the current working directory.

    This is useful for cleaning up the current working directory of a
    datalore notebook.
    """
    print('cwd: ' + str(Path.cwd()))

    fps = Path.cwd().glob('*')

    n2del = {
            '.private'   : None ,
            'lost+found' : None
            }
    fps = [x for x in fps if x.stem not in n2del.keys()]

    print(fps)

    _ = [x.unlink() for x in fps if not x.is_dir()]
    _ = [shutil.rmtree(x) for x in fps if x.is_dir()]

    fps = Path.cwd().glob('*')
    print(list(fps))
