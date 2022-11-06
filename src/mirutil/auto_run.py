"""

    """

import subprocess
from pathlib import Path

from giteasy import GitHubRepo

from .files import read_json_file


class Conf :
    repo_url = 'repo_url'
    python_version = 'python_version'
    module_2_run = "module_2_run"

conf = Conf()

def make_venv(fp = Path('conf.json')) :
    js = read_json_file(fp)

    rp_url = js[conf.repo_url]
    ghr = GitHubRepo(rp_url)

    pyv = js[conf.python_version]

    subprocess.run(['pyenv' , 'install' , '--skip-existing' , pyv])
    subprocess.run(['pyenv' , 'virtualenv-delete' , '-f' , ghr.repo_name])
    subprocess.run(['pyenv' , 'virtualenv' , pyv , ghr.repo_name])

    print(ghr.repo_name)
