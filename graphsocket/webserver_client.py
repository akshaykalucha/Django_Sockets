import sys
import struct
from base64 import b64encode
from hashlib import sha1
import logging
from socket import error as SocketError
import errno

if sys.version_info[0] < 3:
    from SocketServer import ThreadingMixIn, TCPServer, StreamRequestHandler
else:
    from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler

class API():
    
    def run_forever(self):
        try:
            logger.info("Listening on port %d for clients.." % self.port)
            self.serve_forever()
        except KeyboardInterrupt:
            self.server_close()
            logger.info("Server terminated.")
        except Exception as e:
            logger.error(str(e), exc_info=True)
            exit(1)

    def new_client(self, client, server):
        pass

    def client_left(self, client, server):
        pass

    def message_received(self, client, server, message):
        pass

    def set_fn_new_client(self, fn):
        self.new_client = fn

    def set_fn_client_left(self, fn):
        self.client_left = fn

    def set_fn_message_received(self, fn):
        self.message_received = fn

    def send_message(self, client, msg):
        self._unicast_(client, msg)

    def send_message_to_all(self, msg):
        self._multicast_(msg)




@classmethod
def calculate_response_key(cls, key):
    GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    hash = sha1(key.encode() + GUID.encode())
    response_key = b64encode(hash.digest()).strip()
    return response_key.decode('ASCII')

def finish(self):
    self.server._client_left_(self)


def encode_to_UTF8(data):
    try:
        return data.encode('UTF-8')
    except UnicodeEncodeError as e:
        logger.error("Could not encode data to UTF-8 -- %s" % e)
        return False
    except Exception as e:
        raise(e)
        return False


# def try_decode_UTF8(data):
#     try:
#         return data.decode('utf-8')
#     except UnicodeDecodeError:
#         return False
#     except Exception as e:
#         raise(e)