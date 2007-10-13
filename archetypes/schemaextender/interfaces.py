from zope.interface import Interface

class ISchemaExtender(Interface):
    """Interface for adapters that extend the schema.
    """
    
    def getFields():
        """Returns a list of fields to be added to the schema.
        """

class IOrderableSchemaExtender(ISchemaExtender):
    """An orderable version of the schema extender
    """
    
    def getOrder(original):
        """Returns the optionally reordered fields.

        'original' is a dictionary where the keys are the names of
        schemata and the keys are lists of field names, in order.
        
        The method should return a new such dictionary with re-ordered
        lists.
        """