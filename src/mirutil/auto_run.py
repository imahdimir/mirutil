"""

    """

import subprocess
from pathlib import Path

from giteasy import GitHubRepo
from giteasy.github_releases import \
    download_latest_release_of_public_github_repo

from .files import read_json_file


class Conf :
    def_fn = Path('conf.json')
    repo_url = 'repo_url'
    python_version = 'python_version'
    module_2_run = "module_2_run"

conf = Conf()

def make_venv(fp = conf.def_fn) :
    js = read_json_file(fp)

    rp_url = js[conf.repo_url]
    ghr = GitHubRepo(rp_url)

    pyv = js[conf.python_version]

    subprocess.run(['pyenv' , 'install' , '--skip-existing' , pyv])
    subprocess.run(['pyenv' , 'virtualenv-delete' , '-f' , ghr.repo_name])
    subprocess.run(['pyenv' , 'virtualenv' , pyv , ghr.repo_name])

    print(ghr.repo_name)

def ret_dirn(fp = conf.def_fn) :
    js = read_json_file(fp)
    rp_url = js[conf.repo_url]
    dirp = download_latest_release_of_public_github_repo(rp_url)
    print(dirp)

def ret_module_2_run_name(fp = conf.def_fn) :
    js = read_json_file(fp)
    print(js[conf.module_2_run])

def dl_main_bash() :
    rp_url = 'https://github.com/imahdimir/auto-run-bash'
    dirp = download_latest_release_of_public_github_repo(rp_url)
    print(dirp)
