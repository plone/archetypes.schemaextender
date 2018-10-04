# -*- coding: utf-8 -*-
from archetypes.schemaextender.extender import instanceSchemaFactory
from archetypes.schemaextender.interfaces import IExtensible
from plone.app.testing.bbb_at import PloneTestCase
from plone.testing import zca
from Products.Archetypes.public import BaseObject
from zope.component import provideAdapter
from zope.interface import implementer

import unittest


class ASTestCase(PloneTestCase):
    """ Base class for testing archetypes.schemaextender """


@implementer(IExtensible)
class ExtensibleType(BaseObject):
    """A very simple extensible type."""


class TestCase(unittest.TestCase):
    def setUp(self):
        zca.pushGlobalRegistry()
        provideAdapter(instanceSchemaFactory)
        self.instance = ExtensibleType("id")

    def tearDown(self):
        zca.popGlobalRegistry()
