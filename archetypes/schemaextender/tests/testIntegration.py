import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc

from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase.layer import PloneSite

import archetypes.schemaextender

ptc.setupPloneSite()


class TestCase(ptc.FunctionalTestCase):

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

    def clearSchemaCache(self):
        attr = '__archetypes_schemaextender_cache'
        if hasattr(self.portal.REQUEST, attr):
            delattr(self.portal.REQUEST, attr)


def test_suite():
    return unittest.TestSuite([

        doctestunit.DocTestSuite(
           module='archetypes.schemaextender.extender',
           setUp=testing.setUp, tearDown=testing.tearDown),

        ztc.FunctionalDocFileSuite(
            'usage.txt', package='archetypes.schemaextender',
            test_class=TestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
