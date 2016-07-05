from zope.interface import Interface
from zope.interface import implementer
from zope.interface import implementer_only
from zope.interface import implements
from zope.interface.interfaces import IInterface
from zope.component import adapts
from archetypes.schemaextender.tests.base import ExtensibleType
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from Products.Archetypes.interfaces.field import IField


class IHighlighted(Interface):
    """A highlighted content item.
    """


@implementer(ISchemaExtender)
class Extender(object):
    adapts(ExtensibleType)

    fields = []

    def __init__(self, context):
        pass

    def getFields(self):
        return self.fields


@implementer_only(IOrderableSchemaExtender)
class OrderableExtender(Extender):
    adapts(ExtensibleType)

    def getOrder(self, original):
        """"Overly complex logic: put our fields first."""
        if not self.fields:
            return original
        toadd=[]
        for field in self.fields:
            field=field.getName()
            try:
                index=original["default"].index(field)
            except ValueError:
                continue
            del original["default"][index]
            toadd.append(field)

        original["default"]=toadd + original["default"]
        return original


@implementer(ISchemaModifier)
class SchemaModifier(object):
    adapts(ExtensibleType)

    def __init__(self, context):
        pass

    def fiddle(self, schema):
        pass


class MockField:
    if IInterface.providedBy(IField):
        implements(IField)
    else:
        __implements__ = IField
    type = "mock"

    def __init__(self, name="MockField", schemata="default"):
        self.name=name
        self.schemata=schemata

    def toString(self):
        return "MockField"

    def getName(self):
        return self.name
