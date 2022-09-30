"""

    """

from gitignore_parser import parse_gitignore


def make_tex_code_4_forest_tree_fr_rootdir(root_dir , gitignore_fp) :
    flt = parse_gitignore(gitignore_fp)

    def _build(cur_dir , ignore_filter) :
        res = "\n[" + cur_dir.name
        ls = cur_dir.glob('*')
        dirs = [x for x in ls if x.is_dir()]
        dirs = sorted(dirs)
        for d in dirs :
            if not ignore_filter(d) :
                res += _build(d , ignore_filter)
        return res + "]"

    return _build(root_dir , flt).strip()
