from abc import ABC, abstractmethod

class BaseTask(ABC):
    @abstractmethod
    def run(self, mapmem, mapref, mapcon, position, g_rows):
        pass

    @abstractmethod
    def validate(self, mapcon, position):
        pass