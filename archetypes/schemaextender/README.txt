========================
archetypes.schemaxtender
========================

This package allows you to inject new fields into an Archetypes schema, using
an adapter. 

For example, let's say we want to add a tags field to a number of content 
types. The field stores values in an annotation, has a default and accesses
a vocabulary.

For the purposes of the test, we will store the vocabulary and the default
in properties on the site root.

    >>> self.portal.manage_addProperty('tags_vocab', ['A', 'B', 'C'], 'lines')
    >>> self.portal.manage_addProperty('tags_default', ['A', 'B'], 'lines')

Schema extenders are applied by adaptation. One way to achieve that, is to 
use a marker interface on content types that you want to extend, and apply
this selectively, either using the <implements /> ZCML directive, or via
the methods in zope.interface.

    >>> import zope.interface
    >>> class ITaggable(zope.interface.Interface):
    ...     """Taggable content
    ...     """

    >>> from Products.ATContentTypes.content import document
    >>> zope.interface.classImplements(document.ATDocument, ITaggable)

Let's ensure that this applies to a properly created document:

    >>> self.folder.invokeFactory('Document', 'taggable-document')
    'taggable-document'
    
    >>> taggable_doc = getattr(self.folder, 'taggable-document')
    >>> ITaggable.providedBy(taggable_doc)
    True

Now we can set up a schema extender, adding a new LinesField, with a
KeywordWidget, using a custom default method and a custom vocabulary.

    >>> from archetypes.schemaextender.field import ExternalField
    >>> from Products.Archetypes import atapi
    >>> from Products.CMFCore.utils import getToolByName

    >>> class TagsField(ExternalField, atapi.LinesField):
    ...
    ...     def getDefault(self, instance):
    ...         portal_url = getToolByName(instance, 'portal_url')
    ...         portal = portal_url.getPortalObject()
    ...         return portal.getProperty('tags_default')
    ...
    ...     def Vocabulary(self, content_instance):
    ...         portal_url = getToolByName(instance, 'portal_url')
    ...         portal = portal_url.getPortalObject()
    ...         return portal.getProperty('tags_vocab')

By mixing in ExternalField (first!), we get standard accessors and mutators 
which are *not* generated on the class. The default storage is 
AnnotationStorage. Here, we override getDefault() and Vocabulary() to set the 
default and the vocabulary.

Sometimes, we may want to do something quite different - for example, we can
let the field manage a marker interface on the type. Here, we do not need the
ExternalField mixin. Instead, we provide our own accessors and mutators.

    >>> class IHighlighted(zope.interface.Interfaces):
    ...     """A highlighted content item.
    ...     """

    >>> class HighlightedField(atapi.BooleanField):
    ...
    ...     def getAccessor(self, instance):
    ...         def accessor():
    ...             return IHighlighted.providedBy(instance)
    ...         return accessor
    ...
    ...     def getEditAccessor(self, instance):
    ...         return self.getAccessor(instance)
    ...
    ...     def getMutator(self, instance):
    ...         def mutator(value):
    ...             if value and not IHighlighted.providedBy(instance):
    ...                 zope.interface.alsoProvides(instance, IHighlighted)
    ...             else if not value and IHighlighted.providedBy(instance):
    ...                 zope.interface.noLongerProvides(instance, IHighlighted)
    ...         return mutator

