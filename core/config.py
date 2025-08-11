import secrets

fernate_key = b'MkAlXecFzVFn_iOPQ35dO6Xr-sUZvN1Q7W8-TzrgLM5='
# SECRET_KEY = "oceanmtech_pvt_ltd"
SECRET_KEY = "e19bfecb4d4cd97607ccb9fffa388c8e8609d12f3b688d26ea0edd75c4b798e6"
# ALGORITHM = "HS256"
ALGORITHM = "HS512"
ACCESS_TOKEN_EXPIRE_DAYS = 100


def generate_64bit_secret_key():
    # 64 bits = 8 bytes
    return secrets.token_hex(32)  # returns 16-character hex string (8 bytes)

# Example usage
key = generate_64bit_secret_key()
print("Config.py secret key:", key)