from app.core.security import verify_password, hash_password
from string import ascii_letters, digits, punctuation
import random

def password_generator(length: int) -> str:
    symbols = ascii_letters + digits + punctuation
    return ''.join(random.choices(symbols, k=length))

def test_hash_and_verify_password():

    min_length = 0
    max_length = 1000

    for _ in range(10):
        length = random.randint(min_length, max_length)
        password = password_generator(length)
        hashed = hash_password(password)
        assert verify_password(password, hashed)

def test_vefify_wrong_password():
    password = "same_password"
    wrong = "wrong_password"

    hashed = hash_password(password)

    assert not verify_password(wrong, hashed)

def test_same_password_different_hashes():
    password = "same_password"

    hash1 = hash_password(password)
    hash2 = hash_password(password)

    assert hash1 != hash2

def test_hash_not_equal_password():
    password = "password"
    hashed = hash_password(password)

    assert password not in hashed