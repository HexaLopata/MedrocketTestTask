"""Builder classes"""

import abc
from datetime import datetime
from typing import List, Tuple

from medrocket_test_task.model import Todo, User


class UserBuilder(abc.ABC):
    """Abstract user builder"""
    @abc.abstractmethod
    def build(self) -> str:
        """Returns user document"""

    @abc.abstractmethod
    def build_title(self) -> str:
        """Returns document title"""

    @abc.abstractmethod
    def build_tasks(self) -> str:
        """Returns document tasks"""


class DefaultUserBuilder(UserBuilder):
    """Builds User Document"""
    MAX_TASK_LENGTH = 48

    def __init__(self, user: User, date: datetime = None):
        if date is None:
            date = datetime.now()
        self.user = user
        self.date = date

    def build(self) -> str:
        """Returns user document"""
        return (self.build_title() + '\n\n' + self.build_tasks()).strip('\n')

    def build_title(self) -> str:
        """Returns document title"""
        formated_date = self.date.strftime("%d.%m.%Y %H:%M")
        task_count = len(self.user.tasks)
        return (f'Отчёт для {self.user.company_name}.\n'
                f'{self.user.name} <{self.user.email}> {formated_date}\n'
                f'Всего задач: {task_count}')

    def build_tasks(self) -> str:
        """Returns document tasks"""
        if len(self.user.tasks) == 0:
            return ''
        completed_tasks, rest_tasks = self._group_tasks()
        completed_tasks_names = list(map(
            lambda t: f'{self._trim_title(t.title)}',
            completed_tasks,
        ))
        rest_tasks_names = list(map(
            lambda t: f'{self._trim_title(t.title)}',
            rest_tasks,
        ))
        completed_tasks_names = '\n'.join(completed_tasks_names)
        rest_tasks_names = '\n'.join(rest_tasks_names)

        return (f'Завершённые задачи ({len(completed_tasks)}):\n'
                f'{completed_tasks_names}\n\n'
                f'Оставшиеся задачи ({len(rest_tasks)}):\n'
                f'{rest_tasks_names}')

    def _group_tasks(self) -> Tuple[List[Todo], List[Todo]]:
        """
        Groups tasks by completion status\n
        Returns (completed_tasks, rest_tasks)
        """
        completed_tasks = []
        rest_tasks = []
        for task in self.user.tasks:
            if task.completed:
                completed_tasks.append(task)
            else:
                rest_tasks.append(task)
        return (completed_tasks, rest_tasks)

    def _trim_title(self, title: str) -> str:
        if len(title) > DefaultUserBuilder.MAX_TASK_LENGTH:
            return title[0:DefaultUserBuilder.MAX_TASK_LENGTH] + '...'
        return title
