import doctest
import unittest
from plone.app.testing import PloneSandboxLayer
from plone.testing import layered
from plone.testing.z2 import Browser

from plone.app.customerize.testing import \
    PLONE_APP_CUSTOMERIZE_FUNCTIONAL_TESTING

OPTIONFLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE)


class CustomerizeFunctionalTestCase(PloneSandboxLayer):

    layer = PLONE_APP_CUSTOMERIZE_FUNCTIONAL_TESTING

    def afterSetUp(self):
        self.portal.acl_users._doAddUser('admin', 'secret', ['Manager'], [])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                'tests/{0}'.format(test_file),
                package='plone.app.customerize',
                optionflags=OPTIONFLAGS
            ),
            layer=PLONE_APP_CUSTOMERIZE_FUNCTIONAL_TESTING)
        for test_file in ('testBrowserLayers.txt', 'testCustomizeView.txt')
    ])

    return suite
