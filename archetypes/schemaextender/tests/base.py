from Products.Five import fiveconfigure
from Products.Five.zcml import load_config
from Products.PloneTestCase.ptc import setupPloneSite, FunctionalTestCase
from Products.PloneTestCase.layer import PloneSite


setupPloneSite()


class TestCase(FunctionalTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            from archetypes import schemaextender
            load_config('configure.zcml', schemaextender)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

    def clearSchemaCache(self):
        attr = '__archetypes_schemaextender_cache'
        if hasattr(self.portal.REQUEST, attr):
            delattr(self.portal.REQUEST, attr)
