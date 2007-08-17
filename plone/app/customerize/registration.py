from Products.Five.browser import BrowserView
from five.customerize.interfaces import IViewTemplateContainer, ITTWViewTemplate
from five.customerize.browser import mangleAbsoluteFilename
from five.customerize.zpt import TTWViewTemplate
from five.customerize.utils import findViewletTemplate
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.component import getGlobalSiteManager, getUtility
from plone.portlets.interfaces import IPortletRenderer
from os.path import basename

from plone.memoize import forever

def getViews(type):
    """ get all view registrations (stolen from zope.app.apidoc.presentation) """
    gsm = getGlobalSiteManager()
    for reg in gsm.registeredAdapters():
        if (len(reg.required) > 1 and
                reg.required[1] is not None and
                reg.required[1].isOrExtends(type)):
            yield reg

def interfaceName(iface):
    """ return a sensible name for the given interface """
    name = getattr(iface, '__name__', repr(iface))
    return getattr(iface, '__identifier__', name)

@forever.memoize
def templateViewRegistrations():
    regs = []
    for reg in getViews(IBrowserRequest):
        factory = reg.factory
        while hasattr(factory, 'factory'):
            factory = factory.factory
        # TODO: this should really be dealt with using
        # a marker interface on the view factory
        name = getattr(factory, '__name__', '')
        if name.startswith('SimpleViewClass') or \
                name.startswith('SimpleViewletClass') or \
                name.endswith('Viewlet') or \
                IPortletRenderer.implementedBy(factory):
            regs.append(reg)
    return regs

def templateViewRegistrationInfos(regs):
    for reg in regs:
        if ITTWViewTemplate.providedBy(reg.factory):
            zptfile = None
            zcmlfile = None
            name = reg.name
            customized = reg.factory.getId()    # TODO: can we get an absolute url?
        else:
            attr, pt = findViewletTemplate(reg.factory)
            if attr is None:        # skip, if the factory has no template...
                continue
            zptfile = mangleAbsoluteFilename(pt.filename)
            zcmlfile = mangleAbsoluteFilename(reg.info.file)
            name = reg.name or basename(zptfile)
            customized = None
        yield {
            'viewname': name,
            'for': interfaceName(reg.required[0]),
            'type': interfaceName(reg.required[-1]),
            'zptfile': zptfile,
            'zcmlfile': zcmlfile,
            'customized': customized,
        }

def templateViewRegistrationGroups(regs):
    ifaces = {}
    comp = lambda a,b: cmp(a['viewname'], b['viewname'])
    for reg in sorted(templateViewRegistrationInfos(regs), cmp=comp):
        key = reg['for']
        if ifaces.has_key(key):
            ifaces[key]['views'].append(reg)
        else:
            ifaces[key] = { 'name': key, 'views': [reg] }
    return sorted(ifaces.values(), cmp=lambda a,b: cmp(a['name'], b['name']))

def findTemplateViewRegistration(for_name, type_name, viewname):
    for reg in templateViewRegistrations():
        if interfaceName(reg.required[0]) == for_name and \
                interfaceName(reg.required[-1]) == type_name:
           if reg.name == viewname or reg.provided.isOrExtends(IPortletRenderer):
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
    attr, template = findViewletTemplate(reg.factory)
    # TODO: we can't do template.read() here because of a bug in
    # Zope 3's ZPT implementation.
    return open(template.filename, 'rb').read()

def getViewPermissionFromRegistration(reg):
    permissions = getattr(reg.factory, '__ac_permissions__', [])
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

