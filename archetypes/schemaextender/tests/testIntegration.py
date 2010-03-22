from unittest import TestSuite, main
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from archetypes.schemaextender.tests.base import TestCase


def test_suite():
    return TestSuite([

        doctestunit.DocTestSuite(
           module='archetypes.schemaextender.extender',
           setUp=testing.setUp, tearDown=testing.tearDown),

        ztc.FunctionalDocFileSuite(
            'usage.txt', package='archetypes.schemaextender',
            test_class=TestCase),

        ])


if __name__ == '__main__':
    main(defaultTest='test_suite')
