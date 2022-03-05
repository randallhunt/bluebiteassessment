import json
import os
import random
import sys

def load_json_file(name):
    dir = os.path.dirname(sys.modules['__main__'].__file__)
    path = '%s/files/%s' % (dir, name)
    with open(path, 'r') as afile:
        data = afile.read()
    return json.loads(data)

def random_hex(len):
    return '%06x' % random.randrange(16**len)