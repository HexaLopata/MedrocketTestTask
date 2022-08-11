"""Medrocket Junior Python test task"""

from medrocket_test_task.deserializers import TodoDeserializer, UserDeserializer
from medrocket_test_task.logging import Logger
from medrocket_test_task.writers import FileSystemWriter
from medrocket_test_task.builders import DefaultUserBuilder
from medrocket_test_task.providers import APITodoProvider, APIUserProvider


class AppController:
    """Connects all app dependencies"""

    def __init__(self) -> None:
        self.provider = APIUserProvider(
            UserDeserializer(),
            APITodoProvider(
                TodoDeserializer())
        )
        self.builder_class = DefaultUserBuilder
        self.writer_class = FileSystemWriter

    def run(self):
        """Starts controller"""
        users = self.provider.get_users()
        for user in users:
            try:
                builder = self.builder_class(user)
                writer = self.writer_class(user)
                document = builder.build()
                writer.write(document)
            except Exception as error:
                Logger.error(str(error))
        Logger.info('The script has finished working')


if __name__ == '__main__':
    AppController().run()
