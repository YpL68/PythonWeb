from abc import ABC, abstractmethod


class ACli(ABC):
    @abstractmethod
    def show_data(self, *args, **kwargs):
        pass

    @abstractmethod
    def change_data_record(self, *args, **kwargs):
        pass
