# -*- coding: utf-8 -*-
from plone.app.testing.bbb_at import PTC_FUNCTIONAL_TESTING
from plone.testing import layered
from unittest import TestSuite
from zope.component import testing

import doctest


def test_suite():
    return TestSuite(
        [
            doctest.DocTestSuite(
                module='archetypes.schemaextender.extender',
                setUp=testing.setUp,
                tearDown=testing.tearDown,
            ),
            layered(
                doctest.DocFileSuite(
                    'usage.txt', package='archetypes.schemaextender'
                ),
                layer=PTC_FUNCTIONAL_TESTING,
            ),
        ]
    )
