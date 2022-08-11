"""Module for unit-testing"""
from datetime import datetime
import unittest

from medrocket_test_task.builders import DefaultUserBuilder
from medrocket_test_task.deserializers import DeserializationError, TodoDeserializer, \
    UserDeserializer
from medrocket_test_task.model import Todo, User


class BuilderTest(unittest.TestCase):
    """Tests UserBuilder class"""

    def test_builder_builds_correct_title(self):
        """Checks if builder build document title correctly"""
        # arrange
        tasks = []
        user = User(1, 'Name Example', 'admin',
                    'example@gmail.com', 'Company Example', tasks)
        date = datetime.now()
        sut = DefaultUserBuilder(user)
        # act
        result = sut.build_title()
        # assert
        self.assertEqual(result, 'Отчёт для Company Example.\n'
                                 'Name Example <example@gmail.com> '
                                 f'{date.strftime("%d.%m.%Y %H:%M")}\n'
                                 'Всего задач: 0')

    def test_builder_shows_task_count_correctly(self):
        """Checks if builder shows correct count of tasks"""
        self.theory_builder_shows_task_count_correctly(
            [Todo(1, 1, 'task1', False), Todo(
                1, 2, 'task2', True), Todo(1, 3, 'task3', True)]
        )
        self.theory_builder_shows_task_count_correctly(
            [Todo(1, 1, 'task1', True), Todo(1, 2, 'task2', True)]
        )
        self.theory_builder_shows_task_count_correctly(
            [Todo(1, 1, 'task1', False), Todo(1, 2, 'task2', False)]
        )

    def theory_builder_shows_task_count_correctly(self, tasks):
        """
        Theory checking if builder shows correct count of tasks
        """
        # arrange
        user = User(1, 'Name Example', 'admin',
                    'example@gmail.com', 'Company Example', tasks)
        date = datetime.now()
        sut = DefaultUserBuilder(user, date)
        # act
        result = sut.build_title()
        # assert
        self.assertEqual(result, 'Отчёт для Company Example.\n'
                                 'Name Example <example@gmail.com> '
                                 f'{date.strftime("%d.%m.%Y %H:%M")}\n'
                                 f'Всего задач: {len(tasks)}')

    def test_builder_shows_small_tasks_correctly(self):
        """Checks if builder returns correct task part of the document"""
        # arrange
        tasks = [
            Todo(1, 1, 'task1', True),
            Todo(1, 2, 'task2', True),
            Todo(1, 3, 'task3', True),
            Todo(1, 4, 'task4', False),
            Todo(1, 5, 'task5', False),
        ]
        user = User(1, 'Name Example', 'admin',
                    'example@gmail.com', 'Company Example', tasks)
        sut = DefaultUserBuilder(user)
        completed_task_count = len(list(filter(lambda t: t.completed, tasks)))
        rest_task_count = len(tasks) - completed_task_count
        # act
        result = sut.build_tasks()
        # assert
        self.assertEqual(result, f'Завершённые задачи ({completed_task_count}):\n'
                                 'task1\n'
                                 'task2\n'
                                 'task3\n\n'
                                 f'Оставшиеся задачи ({rest_task_count}):\n'
                                 'task4\n'
                                 'task5')

    def test_builder_returns_empty_string_when_0_tasks(self):
        """Checks if builder returns empty task part when user has 0 tasks"""
        # arrange
        tasks = []
        user = User(1, 'Name Example', 'admin',
                    'example@gmail.com', 'Company Example', tasks)
        sut = DefaultUserBuilder(user)
        # act
        result = sut.build_tasks()
        # assert
        self.assertEqual(result, '')

    def test_builder_returns_no_completed_tasks_when_user_has_not_it(self):
        """Checks if builder returns no completed tasks when user has not it"""
        # arrange
        tasks = [Todo(1, 5, 'task1', False),]
        user = User(1, 'Name Example', 'admin',
                    'example@gmail.com', 'Company Example', tasks)
        sut = DefaultUserBuilder(user)
        # act
        result = sut.build_tasks()
        # assert
        self.assertEqual(result, f'Оставшиеся задачи ({len(tasks)}):\n'
                                 'task1')

    def test_builder_returns_no_rest_tasks_when_user_has_not_it(self):
        """Checks if builder returns no rest tasks when user has not it"""
        # arrange
        tasks = [Todo(1, 5, 'task1', True),]
        user = User(1, 'Name Example', 'admin',
                    'example@gmail.com', 'Company Example', tasks)
        sut = DefaultUserBuilder(user)
        # act
        result = sut.build_tasks()
        # assert
        self.assertEqual(result, f'Завершённые задачи ({len(tasks)}):\n'
                                 'task1')

    def test_builder_shows_tasks_with_a_boundary_length_correctly(self):
        """Checks if builder returns correct tasks with boundary length"""
        # arrange
        tasks = [
            Todo(1, 1, '1' * DefaultUserBuilder.MAX_TASK_LENGTH, True),
            Todo(1, 2, '2' * DefaultUserBuilder.MAX_TASK_LENGTH, True),
            Todo(1, 3, 'task3', True),
            Todo(1, 4, 'task4', False),
            Todo(1, 5, '5' * DefaultUserBuilder.MAX_TASK_LENGTH, False),
        ]
        user = User(1, 'Name Example', 'admin',
                    'example@gmail.com', 'Company Example', tasks)
        sut = DefaultUserBuilder(user)
        completed_task_count = len(list(filter(lambda t: t.completed, tasks)))
        rest_task_count = len(tasks) - completed_task_count
        # act
        result = sut.build_tasks()
        # assert
        self.assertEqual(result, f'Завершённые задачи ({completed_task_count}):\n'
                                 f'{"1" * DefaultUserBuilder.MAX_TASK_LENGTH}\n'
                                 f'{"2" * DefaultUserBuilder.MAX_TASK_LENGTH}\n'
                                 'task3\n\n'
                                 f'Оставшиеся задачи ({rest_task_count}):\n'
                                 'task4\n'
                                 f'{"5" * DefaultUserBuilder.MAX_TASK_LENGTH}')

    def test_builder_trims_large_tasks(self):
        """Checks if builder returns correct large tasks"""
        # arrange
        tasks = [
            Todo(1, 1, '1' * (DefaultUserBuilder.MAX_TASK_LENGTH + 10), True),
            Todo(1, 2, '2' * (DefaultUserBuilder.MAX_TASK_LENGTH + 1), True),
            Todo(1, 3, 'task3', True),
            Todo(1, 4, 'task4', False),
            Todo(1, 5, '5' * (DefaultUserBuilder.MAX_TASK_LENGTH + 100), False),
        ]
        user = User(1, 'Name Example', 'admin',
                    'example@gmail.com', 'Company Example', tasks)
        sut = DefaultUserBuilder(user)
        completed_task_count = len(list(filter(lambda t: t.completed, tasks)))
        rest_task_count = len(tasks) - completed_task_count
        # act
        result = sut.build_tasks()
        # assert
        self.assertEqual(result, f'Завершённые задачи ({completed_task_count}):\n'
                                 f'{"1" * DefaultUserBuilder.MAX_TASK_LENGTH}...\n'
                                 f'{"2" * DefaultUserBuilder.MAX_TASK_LENGTH}...\n'
                                 'task3\n\n'
                                 f'Оставшиеся задачи ({rest_task_count}):\n'
                                 'task4\n'
                                 f'{"5" * DefaultUserBuilder.MAX_TASK_LENGTH}...')

    def test_builder_build_whole_document_correctly(self):
        """Checks if builder returns correct final document"""
        # arrange
        tasks = [
            Todo(2, 1, 'distinctio vitae autem nihil ut molestias quo', True),
            Todo(2, 2, 'est ut voluptate quam dolor', True),
            Todo(2, 3, 'suscipit repellat esse quibusdam voluptatem incidunt', False),
            Todo(2, 4, 'laborum aut in quam', False),
        ]
        user = User(2, 'Ervin Howell', 'admin',
                    'Shanna@melissa.tv', 'Deckow-Crist', tasks)
        date = datetime(2020, 9, 23, 15, 25)
        sut = DefaultUserBuilder(user, date)
        # act
        result = sut.build()
        # assert
        self.assertEqual(result, 'Отчёт для Deckow-Crist.\n'
                                 'Ervin Howell <Shanna@melissa.tv> 23.09.2020 15:25\n'
                                 'Всего задач: 4\n\n'
                                 'Завершённые задачи (2):\n'
                                 'distinctio vitae autem nihil ut molestias quo\n'
                                 'est ut voluptate quam dolor\n\n'
                                 'Оставшиеся задачи (2):\n'
                                 'suscipit repellat esse quibusdam voluptatem inci...\n'
                                 'laborum aut in quam')


class TodoDeserializerTest(unittest.TestCase):
    """Tests TodoDeserializer class"""

    def test_deserializer_returns_correct_object_on_valid_input(self):
        """Tests if deserializer returns correct object on valid input"""
        # arrange
        task_dict = {'id': 1, 'user_id': 1,
                     'title': 'test title', 'completed': False}
        task = Todo(1, 1, 'test title', False)
        sut = TodoDeserializer()
        # act
        result = sut.deserealize(**task_dict)
        # assert
        self.assertEqual(result, task)

    def test_deserializer_raises_the_exception_on_empty_dict(self):
        """Tests if deserializer raises the error on empty input"""
        # arrange
        task_dict = dict()
        sut = TodoDeserializer()
        # act and assert
        self.assertRaises(DeserializationError, sut.deserealize, **task_dict)

    def test_deserializer_raises_the_exception_on_invalid_format_input(self):
        """Tests if deserializer raises the error on data in invalid format"""
        self.theory_deserializer_raises_the_exception_on_invalid_format_input(
            {'id': 'NaN', 'user_id': 1, 'title': 'title', 'completed': False}
        )
        self.theory_deserializer_raises_the_exception_on_invalid_format_input(
            {'id': 1, 'user_id': 'NaN', 'title': 'title', 'completed': False}
        )
        self.theory_deserializer_raises_the_exception_on_invalid_format_input(
            {'id': 1, 'user_id': 1, 'title': None, 'completed': False}
        )
        self.theory_deserializer_raises_the_exception_on_invalid_format_input(
            {'id': 1, 'user_id': 1, 'title': 'title', 'completed': 'not bool'}
        )

    def theory_deserializer_raises_the_exception_on_invalid_format_input(self, task_dict):
        """Theory checking if deserializer raises the error on data in invalid format"""
        # arrange
        sut = TodoDeserializer()
        # act and assert
        self.assertRaises(DeserializationError, sut.deserealize, **task_dict)


class UserDeserializerTest(unittest.TestCase):
    """Tests UserDeserializer class"""

    def test_deserializer_returns_correct_object_on_valid_input(self):
        """Tests if deserializer returns correct object on valid input"""
        # arrange
        task_dict = {
            'id': 1,
            'name': 'Leanne Graham',
            'username': 'Bret',
            'email': 'Sincere@april.biz',
            'company': {
                'name': 'Romaguera-Crona',
                'catchPhrase': 'Multi-layered client-server neural-net',
                'bs': 'harness real-time e-markets'
            }
        }
        user = User(1, 'Leanne Graham', 'Bret',
                    'Sincere@april.biz', 'Romaguera-Crona', [])
        sut = UserDeserializer()
        # act
        result = sut.deserealize(**task_dict)
        # assert
        self.assertEqual(result, user)

    def test_deserializer_raises_the_exception_on_empty_dict(self):
        """Tests if deserializer raises the error on empty input"""
        # arrange
        user_dict = dict()
        sut = UserDeserializer()
        # act and assert
        self.assertRaises(DeserializationError, sut.deserealize, **user_dict)

    def theory_deserializer_raises_the_exception_on_invalid_format_input(self, user_dict):
        """Theory checking if deserializer raises the error on data in invalid format"""
        # arrange
        sut = UserDeserializer()
        # act and assert
        self.assertRaises(DeserializationError, sut.deserealize, **user_dict)

    def test_deserializer_raises_the_exception_on_invalid_format_input(self):
        """Tests if deserializer raises the error on data in invalid format"""
        self.theory_deserializer_raises_the_exception_on_invalid_format_input({
            'id': 'NaN',
            'name': 'name',
            'username': 'username',
            'email': 'example@gmail.com',
            'company': {
                'name': 'Romaguera-Crona',
                'catchPhrase': 'Multi-layered client-server neural-net',
                'bs': 'harness real-time e-markets'
            }
        })
        self.theory_deserializer_raises_the_exception_on_invalid_format_input({
            'id': 1,
            'name': None,
            'username': 'username',
            'email': 'example@gmail.com',
            'company': {
                'name': 'Romaguera-Crona',
                'catchPhrase': 'Multi-layered client-server neural-net',
                'bs': 'harness real-time e-markets'
            }
        })
        self.theory_deserializer_raises_the_exception_on_invalid_format_input({
            'id': 1,
            'name': 'name',
            'username': None,
            'email': 'example@gmail.com',
            'company': {
                'name': 'Romaguera-Crona',
                'catchPhrase': 'Multi-layered client-server neural-net',
                'bs': 'harness real-time e-markets'
            }
        })
        self.theory_deserializer_raises_the_exception_on_invalid_format_input({
            'id': 1,
            'name': 'name',
            'username': 'username',
            'email': None,
            'company': {
                'name': 'Romaguera-Crona',
                'catchPhrase': 'Multi-layered client-server neural-net',
                'bs': 'harness real-time e-markets'
            }
        })
        self.theory_deserializer_raises_the_exception_on_invalid_format_input({
            'id': 1,
            'name': 'name',
            'username': 'username',
            'email': 'example@gmail.com',
            'company': None
        })
        self.theory_deserializer_raises_the_exception_on_invalid_format_input({
            'id': 1,
            'name': 'name',
            'username': 'username',
            'email': 'example@gmail.com',
            'company': {
                'name': None,
                'catchPhrase': 'Multi-layered client-server neural-net',
                'bs': 'harness real-time e-markets'
            }
        })
        self.theory_deserializer_raises_the_exception_on_invalid_format_input({
            'id': 1,
            'name': 'name',
            'username': 'username',
            'email': 'example@gmail.com',
            'company': 'string'
        })
