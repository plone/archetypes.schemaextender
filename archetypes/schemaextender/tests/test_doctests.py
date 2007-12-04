import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

import archetypes.schemaextender

# This is used in one of the tests - it needs to be defined here so
# that it can be pickled by the ZODB.


class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             archetypes.schemaextender)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass
    

def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='archetypes.schemaextender',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        doctestunit.DocTestSuite(
           module='archetypes.schemaextender.extender',
           setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='archetypes.schemaextender',
        #    test_class=TestCase),

        ztc.FunctionalDocFileSuite(
            'README.txt', package='archetypes.schemaextender',
            test_class=TestCase),
        
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
