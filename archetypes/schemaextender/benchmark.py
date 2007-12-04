# This is a very simple benchmark to see how schemaextender affects
# the performance of Archetypes.
#
# You can run it like so:
#
#    bin/instance run src/archetypes.schemaextender/archetypes/schemaextender/benchmark.py
#
# the exact path may differ pending your directory layout.

import time
from zope.interface import classImplements
from zope.component import provideAdapter
from zope.component import getGlobalSiteManager
from archetypes.schemaextender.extender import instanceSchemaFactory
from archetypes.schemaextender.interfaces import IExtensible
from archetypes.schemaextender.tests.mocks import ExtensibleType
from archetypes.schemaextender.tests.mocks import Extender
from archetypes.schemaextender.tests.mocks import OrderableExtender
from archetypes.schemaextender.tests.mocks import SchemaModifier



def bench():
    i=5000
    a=ExtensibleType("id")
    start=time.time()
    while i:
        a._updateSchema()
        i-=1
    delta=time.time()-start
    return delta

print "Starting benchmark"
print "Benchmark without atse: %.2f seconds" % bench()

classImplements(ExtensibleType, IExtensible)
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

