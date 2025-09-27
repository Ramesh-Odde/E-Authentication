import random
from typing import Optional


class OTPManager:
    def __init__(self, length: int = 6):
        self.length = length
        self.current_otp = self._generate_new_otp()
    def _generate_new_otp(self) -> str:
        return "".join(str(random.randrange(10)) for _ in range(self.length))

    def get_otp(self) -> str:
        return self.current_otp

    def regenerate(self) -> str:
        self.current_otp = self._generate_new_otp()
        return self.current_otp

    def verify(self, candidate: str) -> bool:
        return candidate == self.current_otp