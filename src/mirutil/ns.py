"""

    """

import json
from pathlib import Path

import githubdata as gd


class Constant :
    ns_repo_url = 'https://github.com/imahdimir/ns'

cte = Constant()

def update_ns_module() :
    py = ''
    if Path('gdu.json').exists() :
        py += ret_gdu_module_code()
        py += '\n'

    if Path('ns.json').exists() :
        py += ret_ns_module_code()

    with open('ns.py' , 'w') as f :
        f.write(py)

def ret_gdu_module_code() :
    with open('gdu.json' , 'r') as f :
        gj = json.load(f)
    return make_class_code_str_fr_dict('GDU' , gj)

def ret_ns_module_code() :
    gds = gd.GithubData(cte.ns_repo_url)
    gds.overwriting_clone()

    with open('ns.json' , 'r') as f :
        ns = json.load(f)

    py = ''
    for k , v in ns.items() :
        jsp = gds.local_path / f'{v}.json'
        with open(jsp , 'r') as f :
            gj = json.load(f)
            py += make_class_code_str_fr_dict(k , gj)
        py += '\n'

    gds.rmdir()
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
    gds = gd.GithubData(cte.ns_repo_url)
    gds.overwriting_clone()

    with open('ns.json' , 'r') as f :
        ns = json.load(f)

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
    with open(json_fp , 'r') as f :
        dct = json.load(f)
    return make_class_fr_dict(dct)

def make_class_instance_fr_json_file(json_fp) :
    cls = make_class_fr_json_file(json_fp)
    return cls()
