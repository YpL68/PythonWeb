from abc import ABC, abstractmethod
from free_assist.function import error_msg


class ACommand(ABC):
    def __init__(self, name: str, params: str = None):
        if self.param_check(params):
            self.name: str = name
            self._params = params if params else ""
            self.interface = None
        else:
            raise ValueError(error_msg(f"Wrong parameters for the command '{name}'"))

    @classmethod
    @abstractmethod
    def param_check(cls, params: str) -> bool:
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
