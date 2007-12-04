import time
from zope.interface import implements
from zope.interface import implementsOnly
from zope.interface import classImplements
from zope.component import adapts
from zope.component import provideAdapter
from zope.component import getGlobalSiteManager
from archetypes.schemaextender.extender import instanceSchemaFactory
from archetypes.schemaextender.interfaces import IExtensible
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from Products.Archetypes.public import BaseObject

class SimpleType(BaseObject):
    """A very simple AT type."""


class Extender(object):
    implements(ISchemaExtender)
    adapts(SimpleType)

    def __init__(self, context):
        pass
    def getFields(self):
        return []

class OrderableExtender(Extender):
    implementsOnly(IOrderableSchemaExtender)
    adapts(SimpleType)

    def getOrder(self, original):
        return original

class SchemaModifier(object):
    implements(ISchemaModifier)
    adapts(SimpleType)
    def __init__(self, context):
        pass
    def fiddle(self, schema):
        pass

def bench():
    i=5000
    a=SimpleType("id")
    start=time.time()
    while i:
        a._updateSchema()
        i-=1
    delta=time.time()-start
    return delta

print "Starting benchmark"
print "Benchmark without atse: %.2f seconds" % bench()

classImplements(SimpleType, IExtensible)
provideAdapter(instanceSchemaFactory)
sm=getGlobalSiteManager()

provideAdapter(Extender, name=u"atse.benchmark")
print "Benchmark with Extender: %.2f seconds" % bench()
sm.unregisterAdapter(Extender, name=u"atse.benchmark")


provideAdapter(OrderableExtender, name=u"atse.benchmark")
print "Benchmark with OrderableExtender: %.2f seconds" % bench()
sm.unregisterAdapter(OrderableExtender, name=u"atse.benchmark")

provideAdapter(SchemaModifier, name=u"atse.benchmark")
print "Benchmark with SchemaModifier: %.2f seconds" % bench()
sm.unregisterAdapter(SchemaModifier, name=u"atse.benchmark")

