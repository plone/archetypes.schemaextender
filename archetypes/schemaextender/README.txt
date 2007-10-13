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

    >>> from Products.Archetypes import atapi
    >>> from Products.CMFCore.utils import getToolByName

    >>> class TagsField(atapi.BooleanField):
    ...
    ...     storage = atapi.AnnotationStorage()
    ...     
    ...     def getDefault(self, instance):
    ...         portal_url = getToolByName(instance, 'portal_url')
    ...         portal = portal_url.getPortalObject()
    ...         return portal.getProperty('tags_default')
    ...     
    ...     def getAccessor(self, instance):
    ...         def accessor():
    ...             return self.get(instance)
    ...         return accessor
    ...
    ...     def getEditAccessor(self, instance):
    ...         def edit_accessor():
    ...             self.storage.get(self.getName(), instance)
    ...         return edit_accessor
    ...
    ...     def getMutator(self, instance):
    ...         def mutator(value):
    ...             self.storage.set(self.getName(), instance, value)
    ...         return mutator



