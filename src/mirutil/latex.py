"""

    """

from gitignore_parser import parse_gitignore


def make_txt4_forest_tree(root_dir , gitignore_fp, only_dirs = True) :
    flt = parse_gitignore(gitignore_fp)

    def _build(cur_dir , ignore_filter , only_dirs) :
        res = "\n[" + cur_dir.name

        ls = cur_dir.glob('*')

        dirs = [x for x in ls if x.is_dir()]
        files = [x for x in ls if not x.is_dir()]

        dirs = sorted(dirs)
        files = sorted(files)

        for d in dirs :
            if not ignore_filter(d) :
                res += _build(d , ignore_filter , only_dirs)
                print(res)

        for f in files :
            if not only_dirs and not ignore_filter(f) :
                res += "[" + f + "]"

        return res + "]"

    return _build(root_dir , flt , only_dirs).strip()
