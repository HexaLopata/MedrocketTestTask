"""Models"""

from dataclasses import dataclass
from typing import List

@dataclass
class Todo:
    """Todo structure"""
    user_id: int
    id: int
    title: str
    completed: bool

@dataclass
class User:
    """User structure"""
    id: int
    name: str
    username: str
    email: str
    company_name: str
    tasks: List[Todo]
