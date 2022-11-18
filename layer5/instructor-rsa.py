# Minimal RSA encrpytion implementation.
#
# The encrpyted message is represented as a Base64 string of bytes,
# represented as a UTF-8 encoded string. This way you can pass around
# the encrypted message as a string instead of a bytearray.


import rsa
import base64

def encrypt(message, public_key):
    """Encrypts a message using RSA.

    Returns a UTF-8 string.

    message - UTF-8 String.
    public_key - rsa.PublicKey.
    """

    message_bytes = message.encode("UTF-8")
    encrypted_bytes = rsa.encrypt(message_bytes, public_key)
    base64_bytes = base64.b64encode(encrypted_bytes)
    base64_str = base64_bytes.decode("UTF-8")
    
    return base64_str

def decrypt(encrypted_message, private_key):
    """Decrypts a message using RSA.

    Returns a UTF-8 string.

    encrypted_message - UTF-8 encoded string (with Base64 representation).
    private_key - rsa.PrivateKey.
    """

    encrypted_b64_bytes = encrypted_message.encode("UTF-8")
    encrypted_bytes = base64.b64decode(encrypted_b64_bytes)
    decrypted_bytes = rsa.decrypt(encrypted_bytes, private_key)
    decrypted_string = decrypted_bytes.decode("UTF-8")
    return decrypted_string


(public_key, private_key) = rsa.newkeys(512)

message = "Good Morning."

e = encrypt(message, public_key)
print (f"Encrypted message:\n{e}")

d = decrypt(e, private_key)
print(f"Decrypted message:\n{d}")
