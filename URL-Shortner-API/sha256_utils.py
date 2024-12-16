import hashlib

def sha256_message(message):
    encoded_message = message.encode()
    return hashlib.sha256(encoded_message).hexdigest()

