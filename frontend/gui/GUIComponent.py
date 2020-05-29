from abc import ABC, abstractmethod

class GUIComponent(ABC):
    @abstractmethod
    def init_components(self, *args, **kwargs):
        pass