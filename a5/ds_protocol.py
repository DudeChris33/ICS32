# ds_protocol.py

# Chris Cyr, Justin Lee
# cyrc@uci.edu, justisl9@uci,edu
# 12436037, 39257953


import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['token', 'userdata'])

# foo = token
# bar = command
# baz = userdata

def encode_json(user: DataTuple) -> str:
    """
    Call the json.dumps function on a DataTuple and returns a json string
    """
    contents = json.dumps(user.userdata)[1:-2]
    output = '{"token": "' + str(user.token) + '", ' + contents + '}}'
    return output