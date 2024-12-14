from abc import ABC, abstractmethod


class GroundVehicle(ABC):

    @abstractmethod
    def move_forward(self, *args, **kwargs):
        pass

    @abstractmethod
    def move_backward(self, *args, **kwargs):
        pass

    @abstractmethod
    def move_right(self, *args, **kwargs):
        pass

    @abstractmethod
    def move_left(self, *args, **kwargs):
        pass

    @abstractmethod
    def stop(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_config_as_json(self, *args, **kwargs):
        pass
