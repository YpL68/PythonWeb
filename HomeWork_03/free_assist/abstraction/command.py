from abc import ABC, abstractmethod


class ACommand(ABC):
    def __init__(self, name: str, params: str = None):
        if self.param_check(params):
            self.name: str = name
            self._params = params if params else ""
            self.data_name = "none"
            self.data = None
            self.interface = None
        else:
            raise ValueError(f"Wrong parameters for the command '{name}'")

    @classmethod
    @abstractmethod
    def param_check(cls, params: str) -> bool:
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
