from Products.Archetypes.interfaces import ISchema, IBaseObject
from archetypes.schemaextender.interface import ISchemaExtender
from zope.component import adapter, getAdapters
from zope.interface import implementer

@implementer(ISchema)
@adapter(IBaseObject)
def instanceSchemaFactory(context):
    """Default schema adapter factory.
    
    In BaseObject, the Schema() method will do 'schema = ISchema(self)'. This
    adapter factory is a replacement of the default one in
    Archetypes.Schema.factory. This one allows you to register named adapter
    to extend the schema. The advantage is that now several packages can do
    additions to the schema without conflicts.
    """
    schema = context.schema.copy()
    extenders = getAdapters((context,), ISchemaExtender)
    for name, extender in extenders:
        fields = extender.getFields()
        for field in fields:
            schema.addField(field)
    return schema
