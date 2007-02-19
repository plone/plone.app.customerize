from Products.Five.browser import BrowserView
from five.customerize.browser import mangleAbsoluteFilename
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.apidoc.presentation import getViews
from zope.component import getGlobalSiteManager


def getViews(type):
    """ get all view registrations (stolen from zope.app.apidoc.presentation) """
    gsm = getGlobalSiteManager()
    for reg in gsm.registeredAdapters():
        if (len(reg.required) > 0 and
                reg.required[-1] is not None and
                reg.required[-1].isOrExtends(type)):
            for required_iface in reg.required[:-1]:
                yield reg


class RegistrationsView(BrowserView):

    def templateViewRegistrations(self):
        for reg in getViews(IBrowserRequest):
            factory = reg.factory
            while hasattr(factory, 'factory'):
                factory = factory.factory
            #XXX this should really be dealt with using a marker interface
            # on the view factory
            if hasattr(factory, '__name__') and \
                   factory.__name__.startswith('SimpleViewClass'):
                yield reg

    def templateViewRegistrationInfos(self):
        def regkey(reg):
            return reg.name
        for reg in sorted(self.templateViewRegistrations(), key=regkey):
            yield {
                'viewname': reg.name,
                'for': getattr(reg.required[0], '__identifier__', '???'),
                'type': getattr(reg.required[1], '__identifier__', '???'),
                'zptfile': mangleAbsoluteFilename(reg.factory.index.filename),
                'zcmlfile': mangleAbsoluteFilename(reg.info.file)
            }
