"""

    """

from pathlib import Path

from giteasy import GitHubRepo

from .files import read_json_file
from .files import write_txt_to_file

class Const :
    ns_repo_url = 'https://github.com/imahdimir/ns'
    ns_py_name = 'ns.py'

cte = Const()

def update_ns_module() :
    py = ''
    if Path('gdu.json').exists() :
        py += ret_gdu_module_code()
        py += '\n'

    if Path('ns.json').exists() :
        py += ret_ns_module_code()

    write_txt_to_file(py , cte.ns_py_name)

def ret_gdu_module_code() :
    gj = read_json_file('gdu.json')
    return make_class_code_str_fr_dict('GDU' , gj)

def read_local_ns_json() :
    return read_json_file('ns.json')

def ret_ns_module_code() :
    ghr = GitHubRepo(cte.ns_repo_url)
    ghr.clone_overwrite()

    ns = read_local_ns_json()

    py = ''
    for k , v in ns.items() :
        jsp = ghr.local_path / f'{v}.json'
        gj = read_json_file(jsp)
        py += make_class_code_str_fr_dict(k , gj)
        py += '\n'

    ghr.rmdir()

    return py

def make_class_code_str_fr_dict(class_name , dct , indent_s_n = 4) :
    st = f'class {class_name} :\n'
    for ky , vl in dct.items() :
        st += ' ' * indent_s_n
        st += f'{ky} = \"{vl}\"'
        st += '\n'
    return st

def make_class_instance_of_ns_classes_instances() :
    dct = make_ns_classes_instances()
    cls = make_class_fr_dict(dct)
    return cls()

def make_ns_classes_instances() :
    gds = GitHubRepo(cte.ns_repo_url)
    gds.clone_overwrite()

    ns = read_local_ns_json()

    o = {}
    for k , v in ns.items() :
        jsp = gds.local_path / f'{v}.json'
        o[k] = make_class_instance_fr_json_file(jsp)

    gds.rmdir()

    return o

def make_class_fr_dict(dct) :
    class TheClass :

        def __init__(self) :
            for k , v in dct.items() :
                setattr(self , k , v)


    return TheClass

def make_class_fr_json_file(json_fp) :
    dct = read_json_file(json_fp)
    return make_class_fr_dict(dct)

def make_class_instance_fr_json_file(json_fp) :
    cls = make_class_fr_json_file(json_fp)
    return cls()

def rm_ns_module() :
    Path(cte.ns_py_name).unlink()
