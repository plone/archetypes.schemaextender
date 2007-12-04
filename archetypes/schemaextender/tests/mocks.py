from zope.interface import implements
from zope.interface import implementsOnly
from zope.component import adapts
from archetypes.schemaextender.tests.case import ExtensibleType
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from Products.Archetypes.interfaces.field import IField

class Extender(object):
    implements(ISchemaExtender)
    adapts(ExtensibleType)

    fields =  []

    def __init__(self, context):
        pass
    def getFields(self):
        return self.fields


class OrderableExtender(Extender):
    implementsOnly(IOrderableSchemaExtender)
    adapts(ExtensibleType)

    def getOrder(self, original):
        original["default"][:0]=[f.getName() for f in self.fields]
        return original


class SchemaModifier(object):
    implements(ISchemaModifier)
    adapts(ExtensibleType)

    def __init__(self, context):
        pass
    def fiddle(self, schema):
        pass


class MockField:
    __implements__ = IField
    type = "mock"
    def __init__(self, name="MockField", schemata="default"):
        self.name=name
        self.schemata=schemata
    def toString(self):
        return "MockField"
    def getName(self):
        return self.name


