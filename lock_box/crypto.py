import hashlib
import base64
import os
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

block_size = 16
IV = block_size * '\x00'
mode = AES.MODE_CBC


def create_key(text):
    if type(text) is str:
        text = text.encode()
    return hashlib.sha256(text).digest()

def generate_key(size=32):
    return os.urandom(size)

# padding methods for blocks


pad = lambda s: s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size).encode()
unpad = lambda s: s[0:-s[-1]]

# AES Code

# generic encryption method for AES


def encrypt_AES(key, payload):

    if type(payload) is str:
        payload = payload.encode()
    raw_payload = pad(payload)
    # generate the cipher for encryption and encrypt
    cipher = AES.new(key, mode, IV=IV)
    encoded_payload = cipher.encrypt(raw_payload)
    # decode back into plain text and return
    return base64.b64encode(encoded_payload).decode('utf-8')

# generic decryption method of AES

def decrypt_AES(key, ecrypted_payload):
    ecrypted_payload = base64.b64decode(ecrypted_payload)
    # generate the cipher for decryption and decrypt
    cipher = AES.new(key, mode, IV=IV)
    decrypted_payload = cipher.decrypt(ecrypted_payload)
    # decode back into plain text, unpad and return
    return unpad(decrypted_payload).decode('utf-8')

# RSA Code
# this will generate the key object which is the private key
# to get the public key once the object is returned just go
# public_key = key.publickey()

def gen_key_RSA():
    random_generator = Random.new().read
    key = RSA.generate(2048, random_generator) # generate pub and priv key
    return key


def encrypt_RSA(public_key, payload):
    if type(payload) is str:
        payload = payload.encode();
    # dont worry about the 32 it is just a random number for compatibility
    encrypted_payload = public_key.encrypt(payload, 32)
    # Extract output from the encoding tuple
    # base64 encode it so we can transfer that data over the wire
    return base64.b64encode(encrypted_payload[0])


def decrypt_RSA(private_key, payload):
    if type(payload) is str:
        payload = payload.encode()
    decrypted_payload = private_key.decrypt(base64.b64decode(payload))
    return decrypted_payload

def import_public_key(public_key):
    if type(public_key) is str:
        public_key = public_key.encode()
    return RSA.importKey(public_key)

def export_public_key(key_pair):
    return key_pair.publickey().exportKey('PEM')

def import_private_key(private_key):
    if type(private_key) is str:
        private_key = private_key.encode()
    return RSA.importKey(private_key)

def export_private_key(key_pair):
    return key_pair.exportKey('PEM')

def sign_text(key_pair, text):
    if type(text) is str:
        text = text.encode()
    chash = create_key(text)
    # for stupid legacy reseasons the function
    # bellow returns a tuple where the first element
    # is the signature
    # and the rest are a hash
    signature = key_pair.sign(chash, b'')
    return signature[0]

def verify_sign(key_pair, signature, text):
    # Because our python libraries for crypto are old we
    # need to wrap the signature in a
    # tuple
    if type(signature) is int:
        signature = (signature, [])
    text_hash = create_key(text)
    return key_pair.verify(text_hash, signature)
