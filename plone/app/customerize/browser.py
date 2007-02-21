from Products.Five.browser import BrowserView
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.traversing.browser import absoluteURL
from zope.component import getSiteManager
from Acquisition import aq_inner
from os.path import sep

from plone.app.customerize import registration
from five.customerize.interfaces import ITTWViewTemplate


class RegistrationsView(BrowserView):

    def getTemplateViewRegistrations(self):
        """ get all global view registrations and cycle through the local
            ones to see which views have already been customized ttw """
        regs = []
        local = {}
        for reg in self.getLocalRegistrations():
            local[(reg.required[0], str(reg.name))] = reg
        for reg in registration.templateViewRegistrations():
            lreg = local.get((reg.required[0], str(reg.name)), None)
            if lreg is not None:
                regs.append(lreg)
            else:
                regs.append(reg)
        return registration.templateViewRegistrationGroups(regs)  

    def getTemplateCodeFromRegistration(self):
        reg = self.getRegistrationFromRequest()
        return registration.getTemplateCodeFromRegistration(reg)

    def getTemplateViewRegistrationInfo(self):
        reg = self.getRegistrationFromRequest()
        return list(registration.templateViewRegistrationInfos([reg]))[0]

    def getRegistrationFromRequest(self):
        form = self.context.request.form
        return registration.findTemplateViewRegistration(form['for_name'],
            form['type_name'], form['view_name'])

    def registerTTWView(self, viewzpt, reg):
        sm = getSiteManager(self.context)
        sm.registerAdapter(viewzpt, required = reg.required,
                           provided = reg.provided, name = reg.name)

    def customizeTemplate(self):
        reg = self.getRegistrationFromRequest()
        viewzpt = registration.customizeTemplate(reg)
        self.registerTTWView(viewzpt, reg)
        url = absoluteURL(aq_inner(viewzpt), self.request) + "/manage_workspace"
        self.request.response.redirect(url)

    def getLocalRegistrations(self):
        components = getSiteManager(self.context)
        for reg in components.registeredAdapters():
            if (len(reg.required) == 2 and
                    reg.required[1].isOrExtends(IBrowserRequest) and
                    ITTWViewTemplate.providedBy(reg.factory)):
                yield reg

