"""Classes providing data"""
import abc
import json
from typing import List

import requests

from medrocket_test_task.deserializers import DeserializationError, Deserializer
from medrocket_test_task.logging import Logger
from medrocket_test_task.model import Todo, User


class UserProvider(abc.ABC):
    """Abstract provider for users"""

    @abc.abstractmethod
    def get_users(self):
        """Returns list of users"""


class TodoProvider(abc.ABC):
    """Abstract provider for todos"""

    @abc.abstractmethod
    def get_todos(self):
        """Returns list of todos"""


class TestProvider(UserProvider):
    """Test Provider"""

    def __init__(self, users: List[User]) -> None:
        self.users = users

    def get_users(self):
        return self.users


class APITodoProvider(TodoProvider):
    """Provides todos from API"""
    TODO_END_POINT: str = 'https://json.medrocket.ru/todos'

    def __init__(self, deserializer: Deserializer) -> None:
        self.deserializer = deserializer

    def get_todos(self):
        data = requests.get(self.TODO_END_POINT)
        data_dicts = json.loads(data.content)
        todos = []
        for data_dict in data_dicts:
            if data_dict.get('userId') is not None:
                data_dict['user_id'] = data_dict['userId']
            try:
                todo = self.deserializer.deserealize(**data_dict)
                todos.append(todo)
            except DeserializationError as error:
                Logger.warn('Invalid data accepted from the server: ' + str(error))
        return todos

class APIUserProvider(UserProvider):
    """Provides users from API"""
    USERS_END_POINT: str = 'https://json.medrocket.ru/users'

    def __init__(self, deserializer: Deserializer, todo_provider: TodoProvider) -> None:
        self.deserializer = deserializer
        self.todo_provider = todo_provider

    def get_users(self):
        data = requests.get(self.USERS_END_POINT)
        data_dicts = json.loads(data.content)
        users = dict()
        for data_dict in data_dicts:
            try:
                user: User = self.deserializer.deserealize(**data_dict)
                users[user.id] = user
            except DeserializationError as error:
                Logger.warn('Invalid data accepted from the server: ' + str(error))

        todos: List[Todo] = self.todo_provider.get_todos()
        for todo in todos:
            user = users[todo.user_id]
            user.tasks.append(todo)

        return list(users.values())
