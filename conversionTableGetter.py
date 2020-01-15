#!/usr/bin/env python3
from abc import ABC, abstractmethod

#abstract class convTable
class conversionTableGetter(ABC):
    '''
        An abstract class to ensure that future classes that load conversion tables have these two guaranteed methods
    '''
    @abstractmethod
    def loadConvTable(self, fileName):
        pass
    
    @abstractmethod
    def parseConvTable(self, **kwargs):
        pass