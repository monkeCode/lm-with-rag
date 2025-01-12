import hashlib
import uuid

def generate_random_hash():
    return uuid.uuid4().hex

def hash_str(s):
    return hashlib.sha256(s.encode("UTF-8")).hexdigest()

if __name__  == "__main__":
    print(generate_random_hash())
    print(hash_str("hello"))