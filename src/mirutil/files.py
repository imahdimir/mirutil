"""

    """

import json


def read_file(fp , mode = 'r' , encoding = 'utf-8') :
    with open(fp , mode , encoding = encoding) as f :
        return f.read()

def read_txt_file(fp , encoding = 'utf-8') :
    return read_file(fp , encoding = encoding)

def read_json_file(fp) :
    return json.loads(read_txt_file(fp))

def write_to_file(content , fp , mode = 'w' , encoding = 'utf-8') :
    if mode == 'w' :
        with open(fp , mode , encoding = encoding) as f :
            f.write(content)
    elif mode == 'wb' :
        with open(fp , mode) as f :
            f.write(content)

def write_txt_to_file(txt , fp) :
    write_to_file(txt , fp)

async def write_to_file_async(content , fp , mode = 'w' , encoding = 'utf-8') :
    write_to_file(content , fp , mode , encoding)

async def write_txt_to_file_async(txt , fp) :
    write_to_file(txt , fp)
