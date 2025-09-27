from dataclasses import dataclass
from typing import Optional




@dataclass
class PersonRecord:
    id_value: str
    name: str
    phone: str
    email: str
    extra1: Optional[str] = None
    extra2: Optional[str] = None