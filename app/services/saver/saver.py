from abc import ABC, abstractmethod

class Saver(ABC):
    def __init__(self, data, save_path):
        self.data = data
        self.save_path = save_path
        
    @abstractmethod
    def save(self, data, save_path):
        pass