from zope.interface import Interface

class ISchemaExtender(Interface):
    """Interface for adapters that extend the schema.
    """
    
    def getFields():
        """Returns fields to be added to the schema."""

    def getOrder(original):
        """Returns the optionally reordered fields.

           Takes a dictionary where the keys are the schema name and the
           values are the names of the fields in original order, returns an
           optionally reordered dictionary.
        """
