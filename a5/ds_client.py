# ds_client.py

# Chris Cyr, Justin Lee
# cyrc@uci.edu, justisl9@uci,edu
# 12436037, 39257953

# server: 168.235.86.101
# port: 3021



from sqlite3 import DatabaseError
from NaClProfile import NaClProfile
from NaClDSEncoder import NaClDSEncoder
import ds_protocol as dsp
import socket, json, Profile


def send(profile: NaClProfile, post: Profile.Post, port: int) -> None:
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    encrypt_entry = salt_profile.encrypt_entry(message, salt_profile.server_public_key)
    msg = dsp.post(salt_profile.public_key, encrypt_entry)
    '''
    profile.dsuserver = "168.235.86.101"
    port = 3021
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((profile.dsuserver, port))

        print(f"Client connected to {profile.dsuserver} on {port}")
        
        join_msg = '{"join": {"username": "' + profile.username + '", "password": "' + profile.password + '", "token": "' + profile.public_key + '"}}'

        send = sock.makefile('w')
        recv = sock.makefile('r')

        send.write(join_msg + '\r\n')
        send.flush()

        resp = recv.readline()
        print("Response:", resp)

        print("Joining on active profile")
        profile.server_public_key = json.loads(resp)['response']['token']
        
        if post != None:
            #encoder = NaClDSEncoder()
            #private_key = encoder.encode_private_key(profile.private_key)
            #public_key = encoder.encode_public_key(profile.public_key)
            #box = encoder.create_box(private_key, public_key)
            msg = str(post.get_entry())
            #dmsg = encoder.decrypt_message(box, msg)
            emsg = profile.encrypt_entry(msg, profile.server_public_key)
            userinfo = {"token": profile.public_key, "post": {"entry": emsg, "timestamp": str(post.get_time())}}
            post = dsp.DataTuple(profile.public_key, userinfo)
            send_msg = dsp.encode_json(post)

            send = sock.makefile('w')
            recv = sock.makefile('r')

            send.write(send_msg + '\r\n')
            send.flush()

            resp = recv.readline()
            print("Response:", resp)

            if "error" not in resp: print('Post successfully uploaded')