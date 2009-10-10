Introduction
============

This package allows you to modify an Archetypes schema, using simple
adapters. This can be used to add new fields, reorder fields and fieldsets
or make other changes.

The most common use of schema extension is to allow add-on products to
enhance standard Plone content types, for example by adding an option
that can be set to toggle special behaviour.

schemaextender hooks into the Archetypes framework by registering
an ISchema adapter for BaseContent and BaseFolder, making it responsible
for providing the schema for all types derived from those classes. This
includes all standard Plone content types. Since only one ISchema adapter
can be active schemaextender provides its own mechanism to modify schemas
using named adapters. Named adapters are allowing to register more than one 
schemaextender per adapted interface.

There are three types of adapters available:

* ISchemaExtender: using this adapter you can add new fields to a schema.

* IOrderableSchemaExtender: this adapters makes it possible to both add
  new fields and reorder fields. This is more costly than just adding new
  fields.

* IBrowserLayerAwareExtender: this adapters are making use of 
  plone.browserlayer, so that the extender is only available if a layer is 
  registered. 

* ISchemaModifier: this is a low-level hook that allows direct manipulation
  of the schema. This can be very dangerous and should never be used if one
  does not know exactly what she/he is doing!


The adapter types are documented in the ''interfaces.py'' file in
archetypes.schemaextender.


Simple example
==============

As an example we will add a simple boolean field to the standard
Plone document type. First we need to create a field class::

     from Products.Archetypes.public import BooleanField
     from archetypes.schemaextender.field import ExtensionField

     class MyBooleanField(ExtensionField, BooleanField):
         """A trivial field."""

schemaextender can not use the standard Archetypes fields directly
since those rely on the class generation logic generating accessors
and mutator methods. By using the ExtensionField mix-in class we can
still use them. Make sure the ExtensionField mix-in comes first, so it
properly overwrites the standard methods.

Next we have to create an adapter that will add this field::

    from zope.component import adapts
    from zope.interface import implements
    from archetypes.schemaextender.interfaces import ISchemaExtender
    from Products.Archetypes.public import BooleanWidget
    from Products.ATContentTypes.interface import IATDocument

    class PageExtender(object):
        adapts(IATDocument)
        implements(ISchemaExtender)


        fields = [
            MyBooleanField("super_power",
            widget = BooleanWidget(
                label="This page has super powers")),
                ]

        def __init__(self, context):
            self.context = context

        def getFields(self):
            return self.fields

Try to store the fields on the class, that way they aren't created each
time the getFields method gets called. Generally you should make sure
getFields does as few things as possible, because it's called very often.

The final step is registering this adapter with the Zope component
architecture. Since we already declared the interface we provide and
which type of object we adapt this can be done very quickly in
configure.zcml (assuming you put the code above in a file extender.py)::

    <configure xmlns="http://namespaces.zope.org/zope"
               xmlns:five="http://namespaces.zope.org/five">

        <include package="archetypes.schemaextender" />
        <adapter factory=".extender.PageExtender" />
    </configure>

Custom fields
=============

If you want you can make more complicated field types as well. The only
requirement is that you need to have ExtensionField as the first parent
class for your field type. As an example here is a field that toggles a
marker interface on an object::

    from zope.interface import Interface
    from zope.interface import alsoProvides
    from zope.interface import noLongerProvides
    from Products.Archetypes.public import BooleanField
    from archetypes.schemaextender.field import ExtensionField

    def addMarkerInterface(obj, *ifaces):
        for iface in ifaces:
            if not iface.providedBy(obj):
                alsoProvides(obj, iface)


    def removeMarkerInterface(obj, *ifaces):
        for iface in ifaces:
            if iface.providedBy(obj):
                noLongerProvides(obj, iface)


    class ISuperPower(Interface):
        """Marker interface for classes that can do amazing things."""


    class InterfaceMarkerField(ExtensionField, BooleanField):
        def get(self, instance, **kwargs):
            return ISuperPower.providedBy(instance)

        def getRaw(self, instance, **kwargs):
            return ISuperPower.providedBy(instance)

        def set(self, instance, value, **kwargs):
            if value:
                addMarkerInterface(instance, ISuperPower)
            else:
                removeMarkerInterface(instance, ISuperPower)


Caching
=======

The package provides an alternative ISchema adapter, which implements a simple
caching strategy to avoid redundant construction of the schema.  To be on the
safe side, the adapter for now only caches individual schemata on the current
request object.  In other words, the cache works per object per request. This
should avoid most potential invalidation problems.

However, as the caching is still experimental and also affects most test
setups, including those of other packages, it is not enabled by default.
Please use the ''caching.zcml'' instead of the regular ''configure.zcml'' to
activate it.  This can be accomplished either via zcml, e.g. from another
package like::

  <include package="archetypes.schemaextender" file="caching.zcml" />

or else via buildout like::

  [instance]
  eggs = archetypes.schemaextender
  zcml = archetypes.schemaextender:caching.zcml

Please also see below for more information about this.

