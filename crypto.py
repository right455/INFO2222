import hashlib
import random
import base64
from cryptography.fernet import Fernet

# Define constants
prime = 2147483647 # Large prime number
root = 5 # Primitive root
salt = "extremelysecureextremely" # Salt


#-----------------------------------------------------------------------------
# Hash
#-----------------------------------------------------------------------------
def salt_hash(string):
    '''
        salt_hash
        Returns the hash value of a given string using string concatenation as the salt
    '''
    global salt

    return hashlib.sha256((salt + string).encode()).hexdigest()

def compare_string_to_hash(string, hash):
    '''
        compare_string_to_hash
        Returns true if the string corresponds to the hash value
    '''
    hashed_string = salt_hash(string)

    if hashed_string == hash:
        return True

    return False

#-----------------------------------------------------------------------------
# Key Generation
#-----------------------------------------------------------------------------
def generate_keys():
    global prime
    global root

    private_key = random.randint(2, prime-2)  # choose a random secret integer
    public_key = pow(root, private_key, prime)  # compute public key

    return private_key, public_key

def compute_key(B, a):
    global prime
    
    K = pow(B, a, prime)  # compute shared secret key
    return K

def encrypt(plaintext, key):
    key_str = str(key)
    key_b64 = base64.urlsafe_b64encode(key_str.encode())
    key_b64_padded = key_b64 + b"=" * ((4 - len(key_b64) % 4) % 4)

    fernet = Fernet(key_b64_padded)

    
    return fernet.encrypt(plaintext.encode())

#print(salt_hash("Password"))
#print(compare_string_to_hash("Password", "2151b2284c6ed0c43b882ebc34d1893682925eedbd6e3c6948718409de34e258"))


#def decrypt(message, key):


a, A = generate_keys()
b, B = generate_keys()

#print(a, A)
#print(b, B)

# Connection between Client1 and Client 2 -->  Generate Keys (public private) Client 1, Client 2 --> Send public keys to server
# Sending messages
print(compute_key(B, a))
print(compute_key(A, b))

#print(encrypt("Hey", compute_key(B, a)))