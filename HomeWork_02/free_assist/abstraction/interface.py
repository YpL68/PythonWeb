from abc import ABC, abstractmethod


class AInterface(ABC):
    @abstractmethod
    def show_table_view(self, *args, **kwargs):
        pass

    @abstractmethod
    def edit_data_record(self, *args, **kwargs):
        pass

    @abstractmethod
    def show_message(self, msg_type: int, msg_str):
        pass
