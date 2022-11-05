"""

    """

import json
import tarfile


def read_file(fp , mode = 'r' , encoding = 'utf-8') :
    if mode == 'rb' :
        with open(fp , mode) as f :
            return f.read()
    with open(fp , mode , encoding = encoding) as f :
        return f.read()

def read_txt_file(fp , encoding = 'utf-8') :
    return read_file(fp , encoding = encoding)

def read_json_file(fp) :
    return json.loads(read_txt_file(fp))

def write_to_file(content , fp , mode = 'w' , encoding = 'utf-8') :
    if mode == 'w' :
        if isinstance(content , bytes) :
            txt = content.decode(encoding)
        else :
            txt = content

        with open(fp , mode , encoding = encoding) as f :
            f.write(txt)

    elif mode == 'wb' :
        with open(fp , mode) as f :
            f.write(content)

def write_txt_to_file(txt , fp) :
    write_to_file(txt , fp)

async def write_to_file_async(content , fp , mode = 'w' , encoding = 'utf-8') :
    write_to_file(content , fp , mode , encoding)

async def write_txt_to_file_async(txt , fp) :
    write_to_file(txt , fp)

def untar_to(src , dst_dir) :
    with tarfile.open(src) as f :
        f.extractall(dst_dir)
