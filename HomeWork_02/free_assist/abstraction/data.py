from abc import ABC, abstractmethod


class ARecord(ABC):
    @classmethod
    @abstractmethod
    def data_view(cls, *args, **kwargs) -> dict:
        pass

    @property
    @abstractmethod
    def values(self) -> list:
        pass

    @abstractmethod
    def match_search_str(self, *args, **kwargs) -> bool:
        pass


class ABook(ABC):
    # @abstractmethod
    # def load_data(self):
    #     pass
    #
    # @abstractmethod
    # def save_data(self):
    #     pass

    @abstractmethod
    def add_record(self, *args, **kwargs) -> str:
        pass

    @abstractmethod
    def get_record(self, *args, **kwargs) -> ARecord:
        pass

    @abstractmethod
    def post_record(self, *args, **kwargs) -> str:
        pass

    @abstractmethod
    def get_record_view(self, *args, **kwargs) -> dict:
        pass

    @abstractmethod
    def post_from_record_view(self, *args, **kwargs) -> str:
        pass

    @abstractmethod
    def del_record(self, *args, **kwargs) -> str:
        pass

    @abstractmethod
    def find_records(self, *args, **kwargs) -> list:
        pass

    @abstractmethod
    def is_record_exists(self, *args, **kwargs) -> bool:
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass
