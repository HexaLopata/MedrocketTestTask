"""Model deserializers"""

import abc
from typing import Dict

from medrocket_test_task.model import Todo, User


class DeserializationError(ValueError):
    """Should be raised when trying to deserialize invalid data"""


class Deserializer(abc.ABC):
    """Deserializes object"""

    @abc.abstractmethod
    def validate_data(self, **kwargs) -> Dict:
        """Validates data"""

    @abc.abstractmethod
    def deserealize(self, **kwargs):
        """Returns object from dict"""


class TodoDeserializer(Deserializer):
    """Deserializes Todos"""

    def validate_data(self, **kwargs) -> Dict:
        """Validates data"""
        if not isinstance(kwargs.get('id'), int):
            raise DeserializationError('Id is not a number')
        if not isinstance(kwargs.get('user_id'), int):
            raise DeserializationError('user_id is not a number')
        if not isinstance(kwargs.get('title'), str):
            raise DeserializationError('Title is not specified')
        if not isinstance(kwargs.get('completed'), bool):
            raise DeserializationError('Completed is not a bool')
        return kwargs

    def deserealize(self, **kwargs):
        """Returns Todo object from dict"""
        data = self.validate_data(**kwargs)
        return Todo(id=data['id'],
                    user_id=data['user_id'],
                    title=data['title'],
                    completed=data['completed'])


class UserDeserializer(Deserializer):
    """Deserializes Todos"""

    def validate_data(self, **kwargs) -> Dict:
        """Validates data"""
        if not isinstance(kwargs.get('id'), int):
            raise DeserializationError('Id is not a number')
        if not isinstance(kwargs.get('name'), str):
            raise DeserializationError('Name is not specified')
        if not isinstance(kwargs.get('username'), str):
            raise DeserializationError('Username is not specified')
        if not isinstance(kwargs.get('email'), str):
            raise DeserializationError('Email is not specified')
        if not isinstance(kwargs['company'], Dict):
            raise DeserializationError('Company is not specified')
        if not isinstance(kwargs['company'].get('name'), str):
            raise DeserializationError('Company name is not specified')
        return kwargs

    def deserealize(self, **kwargs):
        """Returns Todo object from dict"""
        data = self.validate_data(**kwargs)
        return User(
            id=data['id'],
            name=data['name'],
            username=data['username'],
            email=data['email'],
            company_name=data['company']['name'],
            tasks=[]
        )
