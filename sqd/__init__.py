import sqlite3, re
from .utils import _execute
from .errors import *


class Section:
    _execute = _execute
    pattern = re.compile('[_A-Za-z][A-Za-z0-9_]*')
    
    def __init__(self, name, url):
        self.name = name
        self.url = url
        
        
    def set(self, key, value):
        if self.pattern.match(key):
    
            try:
                self._execute(f'insert into {self.name}(key, value) values(?,?)', key, value)
            except sqlite3.IntegrityError:
                self._execute(f'update {self.name} set value = ? where key = \'{key}\'', value)
                
        else:
            raise KeyError(f'key must match the pattern: [A-Za-z_][A-Za-z0-9_]*')
    
    def get(self, key, default = None):
        if self.pattern.match(key):
            result = self._execute(f'select value from {self.name} where key = \'{key}\'', fetch='one')
            
            return default if not result else result[0]
        else:
            raise KeyError(f'key must match the pattern: [A-Za-z_][A-Za-z0-9_]*')
    
    def pop(self, key):
        if self.pattern.match(key):
            result = self._execute(f'select value from {self.name} where key = \'{key}\'', fetch='one')
            
            if result:
                return self._execute(f'delete from {self.name} where key = \'{key}\'')
            else:
                raise KeyError(key)
        
        else:
            raise KeyError(f'key must match the pattern: [A-Za-z_][A-Za-z0-9_]*')
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            self.set(key, value)
    
    def values(self):
        return (x[0] for x in self._execute(f'select value from {self.name}', fetch='all'))
    
    def keys(self):
        return (x[0] for x in self._execute(f'select key from {self.name}', fetch='all'))
    
    def items(self):
        return self._execute(f'select * from {self.name}', fetch='all')
    
    def __str__(self):
        result = {x:y for x, y in self.items()}
        
        return str(result)
        
    def __len__(self):
        return len(self._execute(f'select value from {self.name}', fetch='all'))
   
    def __iter__(self):
        self.__keys = self.keys()
        
        return self
        
    def __next__(self):
        return next(self.__keys)
    
        
    
    
    __setitem__ = set
    __getitem__ = get
    __delitem__ = pop
    

class SQD:
    _execute = _execute
    pattern = re.compile('[_A-Za-z][A-Za-z0-9_]*')
    
    
    def __init__(self, url):
        self.url = url
        
    def create_section(self, name):
        if self.pattern.match(name):
            self._execute(f'create table if not exists {name}(key varchar unique primary key, value varchar)')
        
        else: raise InvalidSectionNameError('section name must match the pattern: [A-Za-z_][A-Za-z0-9_]*')
    
    def delete_section(self, name):
        if self.pattern.match(name):
            try:
                self._execute(f'drop table {name}')
            except sqlite3.OperationalError:
                raise SectionNotFoundError(f'section {name} not found')
                    
        else: raise InvalidSectionNameError('section name must match the pattern: [A-Za-z_][A-Za-z0-9_]*')
        
    def get_section(self, name):
        if self.pattern.match(name):
            try:
                self._execute(f'select * from {name}', fetch='one')
                
                return Section(name, self.url)
            except sqlite3.OperationalError:
                return None
                
        else: raise InvalidSectionNameError('section name must match the pattern: [A-Za-z_][A-Za-z0-9_]*')
    
    
    __getattr__ = get_section
    __getitem__ = get_section
    
    __delattr__ = delete_section
    __delitem__ = delete_section