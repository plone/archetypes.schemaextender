from zope.interface import Interface

class ISchemaExtender(Interface):
    """Interface for adapters that extend the schema"""
    
    def getFields():
        """Return a list of fields to be added to the schema."""

class IOrderableSchemaExtender(ISchemaExtender):
    """An orderable version of the schema extender"""
    
    def getOrder(original):
        """Return the optionally reordered fields.

        'original' is a dictionary where the keys are the names of
        schemata and the values are lists of field names, in order.
        
        The method should return a new such dictionary with re-ordered
        lists.
        """

class ISchemaModifier(Interface):
    """Interface for adapters that modify the existing schema.
    
    Before you're allowed to use this method, you must take the Oath
    of the Schema Modifier. Repeat after us:
    
      "I <name>, hereby do solemnly swear, to refrain, under any 
       circumstances, from using this adapter for Evil. I will not
       delete fields, change field types or do other breakable and evil
       things. Promise."
       
    Okay, then we can all move on.
    """
    
    def fiddle(schema):
        """Fiddle the schema.
        
        This is a copy of the class' schema, with any ISchemaExtender-provided
        fields added. The schema may be modified in-place: there is no
        need to return a value.
        
        In general, it will be a bad idea to delete or materially change 
        fields, since other components may depend on these ones.
        """