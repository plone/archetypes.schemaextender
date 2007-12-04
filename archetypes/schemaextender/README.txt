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
includes all standard Plone content types. Since only know ISchema adapter
can be active schemaextender provides its own mechanism to modify schemas
using named adapters.

There are three types of adapters available:

* ISchemaExtender: using this adapter you can add new fields to a schema.

* IOrderableSchemaExtender: this adapters makes it possible to both add
  new fields and reorder fields. This is more costly than just adding new
  fields.

* ISchemaModifier: this is a low-level hook that allows direct manipulation
  of the schema. This can be very dangerous and should never be used.


The adapter types are documented in the ''interfaces.py'' file in
archetypes.schemaextender.

Simple example
==============

As an example we will add a simple boolean field to the standard
Plone document type. First we need to create a field class::

     from Products.Archetypes.public import BooleanField
     from archetypes.schemaextender.field import ExtensionField

     class MyBoolean(ExtensionField, BooleanField):
        """A trivial field."""

schemaextender can not use the standard Archetypes fields directly
since those rely on the class generation logic generating accessors
and mutator methods. By using the ExtensionField mix-in class we can
still use them.

Next we have to create an adapter that will add this field::

    from zope.component import adapts
    from zope.interface import implements
    from archetypes.schemaextender.interfaces import ISchemaExtender
    from Products.Archetypes.public import BooleanWidget
    from Products.ATContentTypes.content.document import ATDocument

    class PageExtender(object):
        adapts(ATDocument)
        implements(ISchemaExtender)


        fields = [
            MyBoleanField("super_power",
            widget = BooleanWidget(
                label="This page has super powers")),
                ]

         def __init__(self, context):
             self.context = context

         def getFields(self):
             return self.fields

The final step is registering this adapter with the Zope component
architecture. Since we already declared the interface we provide and
which type of object we adapt this can be done very quickly in
configure.zcml::

    <include package="archetypes.schemaextender" />
    <adapter factory=".extender.PageExtender" />



Custom fields
=============

If you want you can make more complicated field types as well. The only
requirement is that you need to have ExtensionField as the first parent
class for your field type. As an example here is a field that toggles a
marker interface on an object::

    def addMarkerInterface(obj, *ifaces):
        for iface in ifaces:
            if not iface.providedBy(obj):
                alsoProvides(obj, iface)

    def removeMarkerInterface(obj, *ifaces):
        for iface in ifaces:
            if iface.providedBy(obj):
                noLongerProvides(obj, iface)

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


