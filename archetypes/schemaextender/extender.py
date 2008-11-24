from Globals import DevelopmentMode
from Products.Archetypes.interfaces import ISchema
from Products.Archetypes.utils import OrderedDict
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import IExtensible
from zope.component import adapter, getAdapters
from zope.interface import implementer
try:
    from plone.browserlayer.utils import registered_layers
    has_plone_browserlayer = True
except ImportError:
    # BBB, for naked plone 3.0, should be removed in future
    has_plone_browserlayer = False

def get_schema_order(schema):
    """Return the order of all schemata and their fields.

    The ordering is returned as an OrderedList for schemata
    with the schemata names as keys fields names as values.
    """
    result = OrderedDict()
    for name in schema.getSchemataNames():
        fields = schema.getSchemataFields(name)
        result[name] = list(x.getName() for x in fields)
    return result


def validate_schema_order(schema, new_order):
    """Update the order of all schemata and their fields.

    The order is given is returned as a dictionary
    with the schemata names as keys fields names as values. It is
    strongly advised to use an OrderedDictionary to prevent the
    schemata from being reorder in unexpected ways.

    It is an error if existing fields do not appear in the new
    ordering, or if fields names are added.
    """

    current_order = get_schema_order(schema)

    current_fields = set()
    for name, fields in current_order.iteritems():
        current_fields = current_fields.union(set(fields))

    new_fields = set()
    for name, fields in new_order.iteritems():
        new_fields = new_fields.union(set(fields))

    if len(current_fields) != len(new_fields):
        raise ValueError, "The number of fields in the new order differs "\
                          "from the number of fields in the schema."

    if current_fields != new_fields:
        raise ValueError, "The set of fields in the new order differs "\
                          "from the set of fields in the schema."

def set_schema_order(schema, new_order):
    """
        >>> from Products.Archetypes import atapi
        >>> schema = atapi.Schema()
        >>> from archetypes.schemaextender import extender
        >>> schema.addField(atapi.BooleanField('boolean1'))
        >>> schema.addField(atapi.BooleanField('boolean2'))
        >>> sorted(extender.get_schema_order(schema).items())
        [('default', ['boolean1', 'boolean2'])]

        >>> extender.set_schema_order(schema, {'default': ['boolean1'],
        ...                                    'foo': ['boolean2']})
        >>> sorted(extender.get_schema_order(schema).items())
        [('default', ['boolean1']), ('foo', ['boolean2'])]

        >>> extender.set_schema_order(schema, {'foo': ['boolean1', 'boolean2']})
        >>> sorted(extender.get_schema_order(schema).items())
        [('foo', ['boolean1', 'boolean2'])]

        >>> extender.set_schema_order(schema, {'foo': ['boolean2', 'boolean1']})
        >>> sorted(extender.get_schema_order(schema).items())
        [('foo', ['boolean2', 'boolean1'])]
    """
    validate_schema_order(schema, new_order)
    for schemata in new_order.keys():
        # iteritems would be nicer, but isnt supported by OrderedDict
        fields = new_order[schemata]
        for name in fields:
            field = schema[name]
            if field.schemata != schemata:
                schema.changeSchemataForField(name, schemata)
            schema.moveField(name, pos='bottom')


@implementer(ISchema)
@adapter(IExtensible)
def instanceSchemaFactory(context):
    """Default schema adapter factory.
    
    In BaseObject, the Schema() method will do 'schema = ISchema(self)'. This
    adapter factory is a replacement of the default one in
    Archetypes.Schema.factory. It allows you to register named adapter
    to extend the schema. The advantage is that now several packages can do
    additions to the schema without conflicts.
    """
    extenders = list(getAdapters((context,), ISchemaExtender))
    modifiers = list(getAdapters((context,), ISchemaModifier))
    if len(extenders) == 0 and len(modifiers) == 0:
        return context.schema

    # as long as the schema is only extended, we can reuse all fields
    # if it's modified later, then we need a full copy, see modifiers below
    # the __add__ functions doesn't copy the field, so we use that by first
    # creating an empty schema of the same class and then add the existing
    # one to it.
    schema = context.schema.__class__() + context.schema

    # loop through all schema extenders
    order = None
    for name, extender in extenders:
        if IBrowserLayerAwareExtender.providedBy(extender) and \
           (not has_plone_browserlayer or \
           extender.layer not in registered_layers()):
            continue
        for field in extender.getFields():
            schema.addField(field)
            if order is not None:
                if not field.schemata in order.keys():
                    order[field.schemata] = list()
                order[field.schemata].append(field.getName())
        if IOrderableSchemaExtender.providedBy(extender):
            if order is None:
                # we need to get the current order first
                order = get_schema_order(schema)
            order = extender.getOrder(order)
            if DevelopmentMode:
                validate_schema_order(schema, order)
    if order is not None:
        set_schema_order(schema, order)

    if len(modifiers) > 0:
        for name, modifier in modifiers:
            if IBrowserLayerAwareExtender.providedBy(modifier) and \
               (not has_plone_browserlayer or \
               modifier.layer not in registered_layers()):
                continue
            modifier.fiddle(schema)

    return schema
