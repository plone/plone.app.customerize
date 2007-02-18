# setup tests with all doctests found in docs/

from plone.app.customerize import docs
from plone.app.customerize.tests import layer
from Testing.ZopeTestCase import FunctionalDocFileSuite
from Products.PloneTestCase import PloneTestCase
from unittest import TestSuite
from os.path import join, abspath, dirname
from os import walk


PloneTestCase.setupPloneSite()

from zope.testing import doctest
OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

class CustomerizeFunctionalTestCase(PloneTestCase.FunctionalTestCase):

    layer = layer.PloneCustomerize
    
    def afterSetUp(self):
        """ set up the tests """
        pass


def test_suite():
    suite = TestSuite()
    docs_dir = abspath(dirname(docs.__file__)) + '/'
    for path, dirs, files in walk(docs_dir):
        for name in files:
            relative = join(path, name)[len(docs_dir):]
            if name.startswith('test') and name.endswith('.txt'):
                suite.addTest(FunctionalDocFileSuite(relative,
                    optionflags=OPTIONFLAGS,
                    package=docs.__name__,
                    test_class=CustomerizeFunctionalTestCase))
    return suite
