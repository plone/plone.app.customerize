from Products.Five.browser import BrowserView
from five.customerize.interfaces import IViewTemplateContainer
from five.customerize.browser import mangleAbsoluteFilename
from five.customerize.zpt import TTWViewTemplate
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.component import getGlobalSiteManager, getUtility


def getViews(type):
    """ get all view registrations (stolen from zope.app.apidoc.presentation) """
    gsm = getGlobalSiteManager()
    for reg in gsm.registeredAdapters():
        if (len(reg.required) > 0 and
                reg.required[-1] is not None and
                reg.required[-1].isOrExtends(type)):
            for required_iface in reg.required[:-1]:
                yield reg

def interfaceName(iface):
    """ return a sensible name for the given interface """
    name = getattr(iface, '__name__', repr(iface))
    return getattr(iface, '__identifier__', name)

def templateViewRegistrations():
    for reg in getViews(IBrowserRequest):
        factory = reg.factory
        while hasattr(factory, 'factory'):
            factory = factory.factory
        # TODO: this should really be dealt with using
        # a marker interface on the view factory
        if hasattr(factory, '__name__') and \
               factory.__name__.startswith('SimpleViewClass'):
            yield reg

def templateViewRegistrationInfos(regs):
    def regkey(reg):
        return reg.name
    for reg in sorted(regs, key=regkey):
        yield {
            'viewname': reg.name,
            'for': interfaceName(reg.required[0]),
            'type': interfaceName(reg.required[1]),
            'zptfile': mangleAbsoluteFilename(reg.factory.index.filename),
            'zcmlfile': mangleAbsoluteFilename(reg.info.file)
        }

def templateViewRegistrationGroups():
    ifaces = {}
    regs = templateViewRegistrations()
    for reg in templateViewRegistrationInfos(regs):
        key = reg['for']
        if ifaces.has_key(key):
            ifaces[key]['views'].append(reg)
        else:
            ifaces[key] = { 'name': key, 'views': [reg] }
    return sorted(ifaces.values(), cmp=lambda a,b: cmp(a['name'], b['name']))

def findTemplateViewRegistration(for_name, type_name, viewname):
    for reg in templateViewRegistrations():
        if interfaceName(reg.required[0]) == for_name and \
           interfaceName(reg.required[1]) == type_name and \
           reg.name == viewname:
            return reg

def generateIdFromRegistration(reg):
    return '%s-%s' % (
        interfaceName(reg.required[0]).lower(),
        reg.name
    )

def getViewClassFromRegistration(reg):
    # The view class is generally auto-generated, we usually want
    # the first base class, though if the view only has one base
    # (generally object or BrowserView) we return the full class
    # and hope that it can be pickled        
    klass = reg.factory
    base = klass.__bases__[0]
    if base is BrowserView or base is object:
        return klass
    return base

def getTemplateCodeFromRegistration(reg):
    template = reg.factory.index
    # TODO: we can't do template.read() here because of a bug in
    # Zope 3's ZPT implementation.
    return open(template.filename, 'rb').read()

def getViewPermissionFromRegistration(reg):
    permissions = reg.factory.__ac_permissions__
    for permission, methods in permissions:
        if methods[0] in ('', '__call__'):
            return permission

def createTTWViewTemplate(reg):
    return TTWViewTemplate(
        id = str(generateIdFromRegistration(reg)),
        text = getTemplateCodeFromRegistration(reg),
        view = getViewClassFromRegistration(reg),
        permission = getViewPermissionFromRegistration(reg))

def customizeTemplate(reg):
    viewzpt = createTTWViewTemplate(reg)
    container = getUtility(IViewTemplateContainer)
    return container.addTemplate(viewzpt.getId(), viewzpt)

