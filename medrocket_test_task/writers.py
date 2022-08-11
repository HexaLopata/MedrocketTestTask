"""Writer classes"""

import abc
import os
from datetime import datetime
from medrocket_test_task.logging import Logger

from medrocket_test_task.model import User


class Writer(abc.ABC):
    """Abstract writer"""

    @abc.abstractmethod
    def write(self, data: str):
        """Writes data"""


class FileSystemWriter(Writer):
    """Writer working with the file system"""
    TASK_DIRECTORY: str = 'tasks'

    def __init__(self, user: User) -> None:
        self.user = user

    def write(self, data: str):
        file_path = os.path.join(
            self.TASK_DIRECTORY, self.user.username + '.txt')
        if os.path.exists(file_path):
            date = self._pull_a_date(file_path)
            new_name = self._rename_old_file(date, file_path)
            self._create_new_file(data, file_path, new_name)
        else:
            self._create_new_file(data, file_path)

    def _pull_a_date(self, file_path: str) -> datetime:
        with open(file_path, 'r', encoding='utf-8') as document:
            document.readline()
            data = document.readline().split()
            date_str, time_str = data[-2], data[-1]

            date = list(map(int, date_str.split('.')))
            time = list(map(int, time_str.split(':')))
            return datetime(year=date[2],
                            month=date[1],
                            day=date[0],
                            hour=time[0],
                            minute=time[1])

    def _rename_old_file(self, date: datetime, path: str) -> str:
        new_name = f'old_{self.user.username}_{date.strftime("%Y-%m-%dT%H:%M")}.txt'
        new_name = os.path.join(self.TASK_DIRECTORY, new_name)
        os.rename(path, new_name)
        return new_name

    def _create_new_file(self, data: str, path: str, renamed_file: str = ''):
        if not os.path.exists(self.TASK_DIRECTORY):
            os.mkdir(self.TASK_DIRECTORY)

        try:
            with open(path, 'x', encoding='utf-8') as document:
                document.write(data)
        except OSError as error:
            if renamed_file:
                try:
                    os.rename(renamed_file, path)
                except OSError as critical_error:
                    Logger.error(
                        'Critical error, impossible to rename old file: ' + str(critical_error))
            Logger.error('Failed to create new file: ' + str(error))
