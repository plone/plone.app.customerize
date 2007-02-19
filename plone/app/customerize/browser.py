from Products.Five.browser import BrowserView
from five.customerize.interfaces import IViewTemplateContainer
from five.customerize.browser import mangleAbsoluteFilename
from five.customerize.zpt import TTWViewTemplate
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.component import getGlobalSiteManager, getSiteManager, getUtility
from os.path import sep


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


class RegistrationsView(BrowserView):

    def templateViewRegistrations(self):
        for reg in getViews(IBrowserRequest):
            factory = reg.factory
            while hasattr(factory, 'factory'):
                factory = factory.factory
            # TODO: this should really be dealt with using
            # a marker interface on the view factory
            if hasattr(factory, '__name__') and \
                   factory.__name__.startswith('SimpleViewClass'):
                yield reg

    def templateViewRegistrationInfos(self):
        def regkey(reg):
            return reg.name
        for reg in sorted(self.templateViewRegistrations(), key=regkey):
            yield {
                'viewname': reg.name,
                'for': interfaceName(reg.required[0]),
                'type': interfaceName(reg.required[1]),
                'zptfile': mangleAbsoluteFilename(reg.factory.index.filename),
                'zcmlfile': mangleAbsoluteFilename(reg.info.file)
            }

    def templateViewRegistrationGroups(self):
        ifaces = {}
        for reg in self.templateViewRegistrationInfos():
            key = reg['for']
            if ifaces.has_key(key):
                ifaces[key]['views'].append(reg)
            else:
                ifaces[key] = { 'name': key, 'views': [reg] }
        return sorted(ifaces.values(), cmp=lambda a,b: cmp(a['name'], b['name']))

    def generateIdFromRegistration(self, reg):
        return '%s-%s' % (
            interfaceName(reg.required[0]).lower(),
            reg.name
        )

    def getViewClassFromRegistration(self, reg):
        # The view class is generally auto-generated, we usually want
        # the first base class, though if the view only has one base
        # (generally object or BrowserView) we return the full class
        # and hope that it can be pickled        
        klass = reg.factory
        base = klass.__bases__[0]
        if base is BrowserView or base is object:
            return klass
        return base

    def getTemplateCodeFromRegistration(self, reg):
        template = reg.factory.index
        # TODO: we can't do template.read() here because of a bug in
        # Zope 3's ZPT implementation.
        return open(template.filename, 'rb').read()

    def getViewPermissionFromRegistration(self, reg):
        permissions = reg.factory.__ac_permissions__
        for permission, methods in permissions:
            if methods[0] in ('', '__call__'):
                return permission

    def createTTWViewTemplate(self, reg):
        return TTWViewTemplate(
            id = str(self.generateIdFromRegistration(reg)),
            text = self.getTemplateCodeFromRegistration(reg),
            view = self.getViewClassFromRegistration(reg),
            permission = self.getViewPermissionFromRegistration(reg))

    def registerTTWView(self, viewzpt, reg):
        sm = getSiteManager(self.context)
        sm.registerAdapter(viewzpt, required = reg.required,
                           provided = reg.provided, name = reg.name)

    def doCustomizeTemplate(self, reg):
        viewzpt = self.createTTWViewTemplate(reg)
        container = getUtility(IViewTemplateContainer)
        viewzpt = container.addTemplate(viewzpt.getId(), viewzpt)
        self.registerTTWView(viewzpt, reg)
        return viewzpt

    def findTemplateViewRegistration(self, for_name, type_name, viewname):
        for reg in self.templateViewRegistrations():
            if interfaceName(reg.required[0]) == for_name and \
               interfaceName(reg.required[1]) == type_name and \
               reg.name == viewname:
                return reg

    def getRegistrationFromRequest(self):
        form = self.context.request.form
        return self.findTemplateViewRegistration(form['for_name'],
            form['type_name'], form['view_name'])
        
    def customizeTemplate(self):
        req = self.getRegistrationFromRequest()
        viewzpt = self.doCustomizeTemplate(req)
        url = sep.join(viewzpt.getPhysicalPath()) + "/manage_workspace"
        self.request.response.redirect(url)

