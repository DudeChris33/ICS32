# NaClProfile.py

# Chris Cyr, Justin Lee
# cyrc@uci.edu, justisl9@uci,edu
# 12436037, 39257953

# C:\Users\Christopher Cyr\Documents\School\First Year\Winter\ICS 32\a5\Chris.dsu

from hashlib import new
import json, os
from NaClDSEncoder import NaClDSEncoder
from Profile import *
from pathlib import Path
from nacl.public import PrivateKey, PublicKey, Box
from copy import copy


class NaClProfile(Profile):
    def generate_keypair(self) -> str:
        """
        Generates a new public encryption key using NaClDSEncoder.
        :return: str
        """
        encoder = NaClDSEncoder()
        encoder.generate()
        self.public_key = encoder.public_key
        self.private_key = encoder.private_key
        self.keypair = encoder.keypair
        return self.keypair

    def import_keypair(self, keypair: str):
        """
        Imports an existing keypair. Useful when keeping encryption keys in a location other than the
        dsu file created by this class.
        """
        self.keypair = keypair
        self.public_key = keypair[:44]
        self.private_key = keypair[44:]

    def add_post(self, post:Post) -> None:
        """
        Override the add_post method to encrypt post entries.
        """
        emsg = self.encrypt_entry(post.get_entry(), self.public_key)
        new_post = Post(emsg)
        super().add_post(new_post)

    def get_posts(self) -> list[Post]:
        """
        Override the get_posts method to decrypt post entries.
        :return: Post
        """
        posts = []
        encoder = NaClDSEncoder()
        private_key = encoder.encode_private_key(self.private_key)
        public_key = encoder.encode_public_key(self.public_key)
        box = encoder.create_box(private_key, public_key)
        for post in self._posts:
            emsg = str(post.get_entry())
            dmsg = encoder.decrypt_message(box, emsg)
            posts.append(Post(dmsg))
        return posts
    
    def save_profile(self, path: str) -> None:
        super().save_profile(path)

    def load_profile(self, path: str) -> None:
        """
        Override the load_profile method to add support for storing a keypair.
        """
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.keypair = obj['keypair']
                self.public_key = obj['public_key']
                self.private_key = obj['private_key']
                if 'server_public_key' in obj.keys(): self.server_public_key = obj['server_public_key']
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()

    def encrypt_entry(self, entry:str, public_key:str) -> str:
        """
        Used to encrypt messages using a 3rd party public key, such as the one that
        the DS server provides.
        :return: bytes
        """
        encoder = NaClDSEncoder()
        prv_key = encoder.encode_private_key(self.private_key)
        pub_key = encoder.encode_public_key(public_key)
        box = encoder.create_box(prv_key, pub_key)
        encoded_entry = encoder.encrypt_message(box, entry)
        return encoded_entry