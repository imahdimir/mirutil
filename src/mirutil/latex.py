"""

    """

import os
from gitignore_parser import parse_gitignore


def ret_pathes_4_latex_dirtree_forest(root_dir ,
                                      gitignore_path ,
                                      only_dirs = True) :
    flt = parse_gitignore(gitignore_path)

    def _build(cur_dir , ignore_filter , only_dirs) :
        res = "\n[" + os.path.basename(cur_dir)

        lst = os.listdir(cur_dir)
        print(lst)

        dirs = [x for x in lst if os.path.isdir(os.path.join(cur_dir , x))]
        files = [x for x in lst if os.path.isfile(os.path.join(cur_dir , x))]

        dirs = sorted(dirs)
        files = sorted(files)

        for d in dirs :
            if not ignore_filter(os.path.join(cur_dir , d)) :
                res += _build(
                        os.path.join(cur_dir , d) , ignore_filter , only_dirs
                        )
                print(res)

        for f in files :
            if not only_dirs and not ignore_filter(os.path.join(cur_dir , f)) :
                res += "[" + f + ", is file]"

        return res + "]"

    return _build(root_dir , flt , only_dirs).strip()
