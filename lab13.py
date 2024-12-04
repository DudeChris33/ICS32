#lab13.py

# Starter code for lab 13 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.
# Please see the README in this repository for the requirements of this lab exercise

# Chris Cyr
# cyrc@uci.edu
# 12436037

import urllib, json
from urllib import request, error, parse
import bookmark_connection as bmc
from bookmark_connection import BookmarkProtocol

"""
The following code snippets can be used to help you prepare your test function:

The url to use for testing. Be sure to run bookmark_server.py before making requests!

url = 'http://localhost:8000'

The format to use for your request data. Don't forget to encode before sending a request!

json = {'data': bmc.BookmarkProtocol.format(BookmarkProtocol(BookmarkProtocol.ADD, data))}
"""

# text = data.encode/decode(encoding = 'utf-8')

def http_api_test(data: str):
    # TODO: write your http connection code here. You can use the above snippets to help
    url = 'http://localhost:8000'
    json = {'data': BookmarkProtocol.format(BookmarkProtocol(BookmarkProtocol.ADD, data))}

    data = parse.urlencode(json)
    data = data.encode('utf-8') 

    headers = {'content-type': 'application/json'}
    req = request.Request(url, data, headers)

    with request.urlopen(req) as response:
        resp = response.read()
        print(resp)
    

if __name__ == '__main__':
    # TODO: call your test code from here. You might try writing a few different url tests.
    http_api_test('https://docs.python.org/3/library/urllib.html')
    http_api_test('https://nuclearsecrecy.com/nukemap/')
    http_api_test('https://cdnb.artstation.com/p/assets/images/images/028/089/623/large/johannes-voss-413496-dog-plains-update.jpg?1593455424')