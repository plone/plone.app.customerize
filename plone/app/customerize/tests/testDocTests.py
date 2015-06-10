# -*- coding: utf-8 -*-
"""Functional Doctests for control panel.
"""
from plone.app.customerize.testing import PLONE_APP_CUSTOMERIZE_FUNCTIONAL_TESTING
from plone.testing import layered
import doctest
import pprint
import unittest2 as unittest


optionflags = (
    doctest.ELLIPSIS |
    doctest.NORMALIZE_WHITESPACE |
    doctest.REPORT_ONLY_FIRST_FAILURE)
testfiles = [
    'testBrowserLayers.txt',
    'testCustomizeView.txt'
]


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                test,
                optionflags=optionflags,
                globs={'pprint': pprint.pprint}
            ),
            layer=PLONE_APP_CUSTOMERIZE_FUNCTIONAL_TESTING
        ) for test in testfiles])
    return suite
