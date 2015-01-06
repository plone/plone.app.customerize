import doctest
from unittest import TestSuite

from plone.testing import layered

from plone.app.customerize.testing import \
    PLONE_APP_CUSTOMERIZE_FUNCTIONAL_TESTING


def test_suite():
    suite = TestSuite()
    OPTIONFLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
    for testfile in ('testBrowserLayers.txt', 'testCustomizeView.txt'):
        suite.addTest(layered(doctest.DocFileSuite(testfile,
                                optionflags=OPTIONFLAGS,
                                package="plone.app.customerize.tests"),
                     layer=PLONE_APP_CUSTOMERIZE_FUNCTIONAL_TESTING))
    return suite
