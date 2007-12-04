import unittest
from zope.interface import implements
from zope.interface import implementsOnly
from zope.component import adapts

from archetypes.schemaextender.tests.case import ExtensibleType
from archetypes.schemaextender.tests.case import TestCase
from zope.component import provideAdapter
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.extender import instanceSchemaFactory
from Products.Archetypes.public import Schema
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

class MockField:
    __implements__ = IField
    type = "mock"
    schemata = "default"
    def toString(self):
        return "MockField"
    def getName(self):
        return "MockField"

class NonExtenderTests(TestCase):
    def testNoExtenderMeansNoChanges(self):
        schema=instanceSchemaFactory(self.instance)
        self.failUnless(schema is self.instance.schema)


class ExtenderTests(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.provideAdapter(Extender, name=u"atse.tests.extender")
        Extender.fields=[]

    def testNopExtender(self):
        schema=instanceSchemaFactory(self.instance)
        self.assertEqual(schema.signature(), self.instance.schema.signature())

    def testExtendWithSingleField(self):
        Extender.fields=[MockField()]
        schema=instanceSchemaFactory(self.instance)
        self.failUnless("MockField" in schema)

    def testExtendTwiceCreateOnce(self):
        Extender.fields=[MockField(), MockField()]
        schema=instanceSchemaFactory(self.instance)
        self.assertEqual(schema.keys().count("MockField"), 1)

class OrderableExtenderTests(ExtenderTests):
    def setUp(self):
        TestCase.setUp(self)
        self.provideAdapter(OrderableExtender, name=u"atse.tests.extender")
        Extender.fields=[]

    def testFieldOrder(self):
        Extender.fields=[MockField()]
        schema=instanceSchemaFactory(self.instance)
        order=[f.getName() for f in schema.getSchemataFields("default")]
        self.assertEqual(order[0], "MockField")

def test_suite():
    suite=unittest.TestSuite()
    suite.addTest(unittest.makeSuite(NonExtenderTests))
    suite.addTest(unittest.makeSuite(ExtenderTests))
    suite.addTest(unittest.makeSuite(OrderableExtenderTests))
    return suite
