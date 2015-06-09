# -*- coding: utf-8 -*-
from plone.app.testing import PloneSandboxLayer
from plone.app.testing.bbb import PTC_FIXTURE
from plone.app.testing.layers import FunctionalTesting


class PloneAppCustomerize(PloneSandboxLayer):
    defaultBases = (PTC_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import plone.app.customerize
        import five.customerize
        self.loadZCML('configure.zcml',
            package=plone.app.customerize)
        self.loadZCML('testing.zcml',
            package=plone.app.customerize.tests)
        self.loadZCML('duplicate_viewlet.zcml',
            package=plone.app.customerize.tests)
        self.loadZCML('configure.zcml',
            package=five.customerize)


PLONE_APP_CUSTOMERIZE_FIXTURE = PloneAppCustomerize()
PLONE_APP_CUSTOMERIZE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_APP_CUSTOMERIZE_FIXTURE,),
    name="PloneAppCustomerize:Functional",
)
