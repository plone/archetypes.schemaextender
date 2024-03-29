Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

3.0.2 (2021-10-07)
------------------

Bug fixes:


- Prevent installation on Python 3, as we know Archetypes does not work there.
  [maurits] (#3330)


3.0.1 (2020-03-21)
------------------

Bug fixes:


- Minor packaging updates. [various] (#1)


3.0.0 (2018-10-31)
------------------

Breaking changes:

- Switch to new TestCase using AT after PloneTestcase is now DX.
  No functionality was changed, but this needs Plone 5.2, so we call it a breaking change.
  [pbauer]


2.1.8 (2018-01-30)
------------------

Bug fixes:

- Add Python 2 / 3 compatibility.  [maurits]


2.1.7 (2017-03-09)
------------------

Bug fixes:

- Update docs about ``Products.ATContentTypes.interfaces`` import location.
  [thet]

- Fix imports from Globals that was removed in Zope4
  [pbauer]

2.1.6 (2016-08-11)
------------------

Fixes:

- Use zope.interface decorator.
  [gforcada]


2.1.5 (2015-03-11)
------------------

- Ported tests to plone.app.testing


2.1.4 (2014-09-08)
------------------

- archetypes.schemaextender assumes presence of getRaw method which
  ComputedField does not provide
  https://dev.plone.org/ticket/11315
  [anthonygerrard]

2.1.3 (2014-02-26)
------------------

- Fix tests [kiorky]

2.1.2 (2013-01-13)
------------------

- PEP8 changes, documentation updates.
  [maurits]

2.1.1 - 2011-07-04
------------------

* Acquire request object via local site hook if object is not
  acquisition-wrapped (in ``cachingInstanceSchemaFactory``). This
  fixes caching issues with objects rendered using DTML. Note that
  this is likely a bug in the ``DocumentTemplate`` code. Ideally, the
  issue should be resolved there.
  [malthe]

2.1 - 2011-01-03
----------------

* Use plone.uuid to look up content UUIDs.
  [toutpt, davisagli]

* Added example of how to use ordered extenders and browser layer aware
  extenders.
  [miohtama]

2.0.3 - 2010-07-07
------------------

* Added back the ``caching.zcml`` file, but have it load ``configure.zcml``.
  This makes it easier to write Plone 3 / 4 compatible code.
  [hannosch]

* Factored out the condition to disable the cache during tests into a module
  global variable called ``CACHE_ENABLED``.
  [hannosch]

2.0.2 - 2010-06-13
------------------

* Changed the schema cache again, to use the id() only as a fallback when there
  is not yet an UID assigned. The id() is unstable with Acquisition wrappers
  and ZODB level ghosting of objects. We provide an explicit API for disabling
  the cache instead.
  [hannosch]

* Avoid deprecation warnings under Zope 2.13.
  [hannosch]

* Change the schema cache key to avoid an issue during content migration when
  there might be two objects that have the same UID but different schemata.
  Now concatenating the Python id() with the UID (id() alone isn't good enough,
  as two objects with non-overlapping lifetimes may have the same id() value).
  Fixes http://dev.plone.org/plone/ticket/10637.
  [davisagli]

2.0.1 - 2010-05-23
------------------

* Disable the schema cache during test runs.
  [hannosch]

2.0 - 2010-05-23
----------------

* Removed the ``caching.zcml`` and enabled caching by default. You can use
  a different caching implementation by using an ``overrides.zcml`` file.
  [hannosch]

* Added ``z3c.autoinclude`` entry point to mark this as a Plone plugin.
  [hannosch]

1.6 - 2010-03-22
----------------

* Fix index accessor to support setting custom accessor methods.
  [witsch]

1.5 - 2009-11-18
----------------

* Fixed test failure in usage.txt.
  [hannosch]

* Standardized package metadata layout.
  [hannosch]

1.4 - 2009-11-05
----------------

* Fix schema copying to also include properties and layers.
  [maerteijn]

1.3 - 2009-10-20
----------------

* Refactored the TranslatableExtensionField getMutator to directly reuse the
  generatedMutatorWrapper from LinguaPlone itself. This avoids duplicating the
  logic and lets schemaextender fields use the special reference field
  handling introduced in LinguaPlone. This change introduces a version
  requirement for LinguaPlone of at least 3.0b6.
  [hannosch]

1.2 - 2009-10-10
----------------

* Add `ISchema` adapter using simple caching on the request in order to
  avoid redundant calculation of the (extended) schema.  The adapter is
  not enabled by default and can be activated by loading `caching.zcml`.
  [witsch]

* Avoid using the overridden `+` operator when copying the original schema
  as this will needlessly validate all fields again.
  [witsch]

* Added missing changelog entry.
  [hannosch, woutervh]

1.1 - 2009-06-03
----------------

* Added support for LinguaPlone language independent fields, by seamlessly
  using a new TranslatableExtensionField when LP is installed.
  [hannosch]

* Added a proper interface to the IExtensionField.
  [hannosch]

* Adjusted tests for Plone 3.3.
  [hannosch]

* Minor adjustment in documentation: a) don't adapt the class in the example,
  b) explain why named adapters are used.
  [jensens]

* Schema modifiers now also browserlayer-aware.
  [jessesnyder]

1.0 - 2008-07-17
----------------

* No changes since 1.0rc1.

1.0rc1 - 2008-04-07
-------------------

* Added optional plone.browserlayer support. Extenders implementing
  IBrowserLayerAwareExtender need to have a layer attribute. Those extenders
  are taken into account only if the specified layer is active.
  [jensens]

1.0b1 - 2007-12-07
------------------

* Schema modifiers implementing ISchemaModifier are now responsible for
  copying fields they modify. See README and the doc strings.
  [fschulze]

* Added a simple benchmark and made some optimizations by avoiding a lot
  of field copying.
  [fschulze, wiggy]

* Use a marker interface instead of overrides.zcml - this means you don't
  need to muck with overrides in dependent products.
  [optilude]

* Added code to allow addition of new schemata. We need an ordered
  dictionary to not bork the order of the schemata.
  [jensens]

* Add a small benchmark utility.
  [wichert]

* Replace the high-level test with unit-tests and extend the test coverage.
  [wichert]

* Rewrite the README to be more human readable.
  [wichert]


1.0a1 - 2007-10-15
------------------

* First public release.
