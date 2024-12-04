# ds_messenger.py

# Chris Cyr, Justin Lee
# cyrc@uci.edu, justisl9@uci,edu
# 12436037, 39257953

from pathlib import Path
import ds_protocol as dsp
import Profile, time, os, json, socket


class NoRecipientError(Exception):
    pass


class DirectMessage(Profile.Post):
    def __init__(self, entry: str = "", timestamp: float = 0, recipient: str = ""):
        self._timestamp = timestamp
        self.set_entry(entry)
        self.set_recipient(recipient)
    
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp, recipient=self._recipient)
    
    def set_recipient(self, recipient):
        self._recipient = recipient
        dict.__setitem__(self, 'recipient', recipient)

        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_recipient(self) -> str:
        return self._recipient
    
    recipient = property(get_recipient, set_recipient)


class NaClProfile(Profile.Profile):
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.bio = ''
        self._posts = []
    
    def add_post(self, post: DirectMessage):
        self._posts.append(post)

    def get_posts(self) -> list[DirectMessage]:
        return self._posts

    def load_profile(self, path: str):
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                for post_obj in obj['_posts']:
                    post = DirectMessage(post_obj['entry'], post_obj['timestamp'], post_obj['recipient'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise Profile.DsuProfileError(ex)
        else:
            raise Profile.DsuFileError()


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.token = ""
        self.port = 3021
        self.sock = socket.socket
        self.recipient = ""

    def send(self, message:str = "", recipient:str = "") -> bool:
        '''
        Returns true if message successfully sent, false if send failed.
        '''
        self.recipient = recipient
        assert type(self.sock) == socket.socket
        send_msg = '{"token": "' + str(self.token) + '", "directmessage": {"entry": "' + str(message) + '", "recipient": "' + str(recipient) + '", "timestamp": "' + str(time.time()) + '"}}'

        send = self.sock.makefile('w')
        recv = self.sock.makefile('r')

        send.write(send_msg + '\r\n')
        send.flush()

        resp = recv.readline()
        #print("Response:", resp)
        self.sock.close()
        
        if "Direct message sent" in resp: return True
        else: return False
        
        
    def retrieve_new(self) -> list:
        '''
        Returns a list of DirectMessage objects containing all new messages
        '''
        assert type(self.sock) == socket.socket
        send_msg = '{"token": "' + str(self.token) + '", "directmessage": "new"}'

        send = self.sock.makefile('w')
        recv = self.sock.makefile('r')

        send.write(send_msg + '\r\n')
        send.flush()

        resp = recv.readline()
        self.sock.close()

        if 'messages' in resp: return json.loads(resp)['response']['messages']
        else: print("ERROR: Response:", resp)

    def retrieve_all(self) -> list:
        '''
        Returns a list of DirectMessage objects containing all messages
        '''
        assert type(self.sock) == socket.socket
        send_msg = '{"token": "' + str(self.token) + '", "directmessage": "all"}'

        send = self.sock.makefile('w')
        recv = self.sock.makefile('r')

        send.write(send_msg + '\r\n')
        send.flush()

        resp = recv.readline()
        self.sock.close()

        if 'messages' in resp: return json.loads(resp)['response']['messages']
        else: print("ERROR: Response:", resp)