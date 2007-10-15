from Products.Archetypes import atapi

class ExtensionField(object):
    """Mix-in class to make Archetypes fields not depend on generated
    accessors and mutators, and use AnnotationStorage by default.
    
    See README.txt for more information.
    """
    
    storage = atapi.AnnotationStorage()
    
    def getAccessor(self, instance):
        def accessor(**kw):
            return self.get(instance, **kw)
        return accessor

    def getEditAccessor(self, instance):
        def edit_accessor(**kw):
            return self.getRaw(instance, **kw)
        return edit_accessor

    def getMutator(self, instance):
        def mutator(value, **kw):
            self.set(instance, value, **kw)
        return mutator

    def getIndexAccessor(self, instance):
        if getattr(self, 'index_method', None) == '_at_edit_accessor':
            return self.getEditAccessor(instance)
        else:
            return self.getAccessor(instance)
