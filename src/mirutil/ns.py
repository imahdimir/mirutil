"""

    """

import json

import githubdata as gd


class Constant :
    ns_repo_url = 'https://github.com/imahdimir/ns'

cte = Constant()

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
