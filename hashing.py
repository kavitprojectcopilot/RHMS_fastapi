from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

class Hash():
    @staticmethod
    def encrypt(password: str):        
        return ph.hash(password)
    
    @staticmethod    
    def verify(hashed_password: str, plain_password: str):        
        try:
            return ph.verify(hashed_password, plain_password)
        except VerifyMismatchError:
            return False