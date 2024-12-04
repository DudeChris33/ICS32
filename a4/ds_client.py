# ds_client.py

# Chris Cyr
# cyrc@uci.edu
# 12436037

# server: 168.235.86.101
# port: 3021

# 0D9E


import socket, time
from sqlite3 import DatabaseError
import ds_protocol as dsp


def send(server: str, port: int, username: str, password: str, msg: dict, bio: str = None) -> bool:
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server, port))

            print(f"Client connected to {server} on {port}")
            
            join_msg = '{"join": {"username": "' + username + '", "password": "' + password + '", "token": ""}}'

            send = sock.makefile('w')
            recv = sock.makefile('r')

            send.write(join_msg + '\r\n')
            send.flush()

            resp = recv.readline()

            print("Joining on active profile")
            token = dsp.extract_token(resp)
            
            if msg != None:
                userinfo = {"post": {"entry": msg["entry"], "timestamp": str(msg["timestamp"])}}
                post = dsp.DataTuple(token, userinfo)
                send_msg = dsp.encode_json(post)

                send = sock.makefile('w')
                recv = sock.makefile('r')

                send.write(send_msg + '\r\n')
                send.flush()

                resp = recv.readline()
                # print("Response:", resp)

                print('Post successfully uploaded')
                
            if bio != None:
                userinfo = {"bio": {"entry": bio, "timestamp": str(time.time())}}
                post = dsp.DataTuple(token, userinfo)
                send_msg = dsp.encode_json(post)

                send = sock.makefile('w')
                recv = sock.makefile('r')

                send.write(send_msg + '\r\n')
                send.flush()

                resp = recv.readline()
                # print("Response:", resp)

                print('Bio successfully uploaded')

            return True
    except Exception as ex:
        print(ex)
        return False