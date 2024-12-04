# ds_protocol.py

# Chris Cyr, Justin Lee
# cyrc@uci.edu, justisl9@uci,edu
# 12436037, 39257953

import socket, json


def join(port: int, dsuserver: str, username: str, password: str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((dsuserver, port))
    print(f"Client connected to {dsuserver} on {port}")
    
    join_msg = '{"join": {"username": "' + str(username) + '", "password": "' + str(password) + '", "token": ""}}'

    send = sock.makefile('w')
    recv = sock.makefile('r')

    send.write(join_msg + '\r\n')
    send.flush()

    resp = recv.readline()
    print("Response:", resp)

    print("Joining on active profile")
    token = json.loads(resp)['response']['token']
    return token, sock