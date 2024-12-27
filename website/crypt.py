from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from os import urandom
from pathlib import Path
import secrets
import string

KEY_FOLDER = Path(__file__).resolve().parent / 'keys'

SAFE_PUNCTUATION = "!#$%&()*+,-./:;<=>?@[]^_{|}~"
CHARSET = string.ascii_letters + string.digits + SAFE_PUNCTUATION


def random_password(length: int = 32) -> str:
    return ''.join(secrets.choice(CHARSET) for _ in range(length))


def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    return kdf.derive(password.encode())


def encrypt_bytes(data: bytes | str, password: str) -> bytes:
    if isinstance(data, str):
        data = data.encode()
    salt = urandom(16)
    key = _derive_key(password, salt)
    iv = urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend()).encryptor()
    encrypted_data = cipher.update(data) + cipher.finalize()
    return salt + iv + encrypted_data


def decrypt_bytes(data: bytes, password: str, return_as_str: bool = False) -> bytes | str:
    salt, iv, encrypted_data = data[:16], data[16:32], data[32:]
    key = _derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend()).decryptor()
    decrypted_data = cipher.update(encrypted_data) + cipher.finalize()
    return decrypted_data.decode() if return_as_str else decrypted_data

'''

    The following code is currently redundant.

def create_async_keypair(password: str, filename: str):

    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()

    with open(KEY_FOLDER / "private" / f"{filename}.pem", "wb") as private_file:
        private_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(password.encode())
        ))

    with open(KEY_FOLDER / "public" / f"{filename}.pem", "wb") as public_file:
        public_file.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))


def async_encrypt(data: bytes | str, filename: str) -> bytes:

    with open(KEY_FOLDER / "public" / f"{filename}.pem", "rb") as public_file:
        public_key = serialization.load_pem_public_key(public_file.read(), backend=default_backend())

    if isinstance(data, str):
        data = data.encode('utf-8')

    return public_key.encrypt(data, padding.OAEP(
        mgf=padding.MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None))


def async_decrypt(data: bytes, password: str, filename: str, return_as_str: bool = False) -> bytes | str:

    with open(KEY_FOLDER / "private" / f"{filename}.pem", "rb") as private_file:
        private_key = serialization.load_pem_private_key(private_file.read(),
                                                         password=password.encode(),
                                                         backend=default_backend())

    decrypted_data = private_key.decrypt(data, padding.OAEP(
        mgf=padding.MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None))

    return decrypted_data.decode() if return_as_str else decrypted_data


def delete_keypair(filename: str):
    public = KEY_FOLDER / "public" / f"{filename}.pem"
    private = KEY_FOLDER / "private" / f"{filename}.pem"
    if public.exists():
        public.unlink()
    if private.exists():
        private.unlink()
'''
