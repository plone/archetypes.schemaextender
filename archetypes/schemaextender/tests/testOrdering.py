import unittest
from Products.Archetypes.public import Schema
from Products.Archetypes.public import ManagedSchema
from archetypes.schemaextender.extender import get_schema_order
from archetypes.schemaextender.tests.mocks import MockField

class GetSchemaOrderTests(unittest.TestCase):
    def testEmptySchema(self):
        schema=Schema()
        self.assertEqual(get_schema_order(schema), {})

    def testSchemataOrdering(self):
        schema=ManagedSchema()
        schema.addField(MockField("one", "one"))
        schema.addField(MockField("two", "two"))
        order=get_schema_order(schema)
        self.assertEqual(order, {"two": ["two"], "one": ["one"]})
        self.assertEqual(order.keys(), ["one", "two"])

        schema.moveSchemata("two", -1)
        order=get_schema_order(schema)
        self.assertEqual(order, {"two": ["two"], "one": ["one"]})
        self.assertEqual(order.keys(), ["two", "one"])

    def testFieldOrdering(self):
        schema=Schema()
        schema.addField(MockField("one"))
        schema.addField(MockField("two"))
        order=get_schema_order(schema)
        self.assertEqual(order, {"default": ["one", "two"]})

        schema.moveField("one", 1)
        order=get_schema_order(schema)
        self.assertEqual(order, {"default": ["two", "one"]})


def test_suite():
    suite=unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetSchemaOrderTests))
    return suite
