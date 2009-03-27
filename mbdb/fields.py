from django.db import models
from django.conf import settings

try:
    import cPickle as pickle
except ImportError:
    import pickle

class PickledObject(str):
    """A subclass of string so it can be told whether a string is
       a pickled object or not (if the object is an instance of this class
       then it must [well, should] be a pickled one)."""
    pass

class PickledObjectField(models.Field):
    __metaclass__ = models.SubfieldBase
    
    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, PickledObject):
            # If the value is a definite pickle; and an error is raised in
            # de-pickling it should be allowed to propogate.
            return pickle.loads(str(value))
        else:
            try:
                return pickle.loads(str(value))
            except:
                # If an error was raised, just return the plain value
                return value
    
    def get_db_prep_save(self, value):
        if value is not None and not isinstance(value, PickledObject):
            if isinstance(value, str):
                # normalize all strings to unicode, like django does
                value = unicode(value)
            value = PickledObject(pickle.dumps(value))
        return value
    
    def get_internal_type(self): 
        return 'TextField'
    
    def get_db_prep_lookup(self, lookup_type, value):
        if lookup_type in ['exact', 'isnull']:
            value = self.get_db_prep_save(value)
            return super(PickledObjectField, self).get_db_prep_lookup(lookup_type, value)
        elif lookup_type == 'in':
            value = [self.get_db_prep_save(v) for v in value]
            return super(PickledObjectField, self).get_db_prep_lookup(lookup_type, value)
        else:
            raise TypeError('Lookup type %s is not supported.' % lookup_type)

class ListField(models.Field):
    __metaclass__ = models.SubfieldBase
    
    def to_python(self, value):
        if hasattr(value, 'split'):
            if settings.DATABASE_ENGINE != 'mysql':
                value = value.decode('unicode-escape')
            return value.split('\0')
        return value
    
    def get_db_prep_save(self, value):
        rv = '\0'.join(value)
        if settings.DATABASE_ENGINE != 'mysql':
            rv = rv.encode('unicode-escape')
        return rv
    
    def get_internal_type(self): 
        return 'TextField'
    
    def get_db_prep_lookup(self, lookup_type, value):
        if lookup_type in ['exact', 'isnull']:
            value = self.get_db_prep_save(value)
            return super(ListField, self).get_db_prep_lookup(lookup_type, value)
        elif lookup_type == 'in':
            value = [self.get_db_prep_save(v) for v in value]
            return super(ListField, self).get_db_prep_lookup(lookup_type, value)
        else:
            raise TypeError('Lookup type %s is not supported.' % lookup_type)