from abc import ABC, abstractmethod

class ICrud(ABC):
    @abstractmethod
    def crear(self, **kwargs):
        pass
    
    @abstractmethod
    def obtener_por_id(self, id):
        pass
    
    @abstractmethod
    def obtener_todos(self):
        pass
    
    @abstractmethod
    def actualizar(self, id, **kwargs):
        pass
    
    @abstractmethod
    def eliminar(self, id):
        pass
    
    @abstractmethod
    def relacion(self, **kwargs):
        pass