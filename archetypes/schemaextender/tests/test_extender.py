import unittest
from zope.interface import implements
from zope.component import adapts

from archetypes.schemaextender.tests.case import NonExtensibleType
from archetypes.schemaextender.tests.case import ExtensibleType
from archetypes.schemaextender.tests.case import TestCase
from zope.component import provideAdapter
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.extender import instanceSchemaFactory
from Products.Archetypes.public import Schema

class Extender(object):
    implements(ISchemaExtender)
    adapts(ExtensibleType)

    def __init__(self, context):
        pass
    def getFields(self):
        return []



class ExtenderTests(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.provideAdapter(Extender, name=u"atse.tests.extender")
        self.normal=NonExtensibleType("id")
        self.extensible=ExtensibleType("id")

    def testNonExtensibleTypes(self):
        schema=instanceSchemaFactory(self.normal)
        self.failUnless(schema is self.normal.schema)

    def testExtensibleType(self):
        schema=instanceSchemaFactory(self.extensible)
        self.failUnless(schema is not self.normal.schema)




def test_suite():
    suite=unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ExtenderTests))
    return suite
