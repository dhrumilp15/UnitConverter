from abc import ABC, abstractmethod

#abstract class convTable
class conversionTableGetter(ABC):
    
    @abstractmethod
    def loadConvTable(self, fileName):
        pass
    
    @abstractmethod
    def parseConvTable(self, **kwargs):
        pass