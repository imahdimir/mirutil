"""

    """

import shutil
from pathlib import Path

from giteasy import GitHubRepo


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

def clone_repo_in_datalore_cwd(repo_url) :
    """Clone a git repository into the current working directory of a datalore notebook."""
    ghr = GitHubRepo(repo_url , local_path = Path.cwd())
    ghr.clone_overwrite()
