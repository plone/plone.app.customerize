# -*- coding: utf-8 -*-
from plone.app.customerize.testing import (
    PLONE_APP_CUSTOMERIZE_FUNCTIONAL_TESTING  # noqa
)
from plone.testing import layered
from unittest import TestSuite

import doctest
import re
import six


class Py23DocChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if six.PY2:
            got = re.sub('NotFound', 'zExceptions.NotFound', got)
            got = re.sub("u'(.*?)'", "'\\1'", got)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


def test_suite():
    suite = TestSuite()
    OPTIONFLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    for testfile in ('testBrowserLayers.txt', 'testCustomizeView.txt'):
        suite.addTest(
            layered(
                doctest.DocFileSuite(
                    testfile,
                    optionflags=OPTIONFLAGS,
                    package='plone.app.customerize.tests',
                    checker=Py23DocChecker(),
                ),
                layer=PLONE_APP_CUSTOMERIZE_FUNCTIONAL_TESTING,
            )
        )
    return suite
