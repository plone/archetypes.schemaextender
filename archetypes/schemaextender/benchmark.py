import time
from zope.interface import implements
from zope.interface import classImplements
from zope.component import adapts
from zope.component import provideAdapter
from archetypes.schemaextender.extender import instanceSchemaFactory
from archetypes.schemaextender.interfaces import IExtensible
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from Products.Archetypes.public import BaseObject

class SimpleType(BaseObject):
    """A very simple AT type."""


class DummyExtender(object):
    implements(IOrderableSchemaExtender)
    adapts(SimpleType)

    def __init__(self, context):
        pass
    def getFields(self):
        return []
    def getOrder(self, original):
        return original

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
provideAdapter(DummyExtender, name=u"atse.benchmark")

print "Benchmark with atse: %.2f seconds" % bench()

