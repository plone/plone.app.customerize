from Products.Five.browser import BrowserView
from zope.component import getSiteManager
from os.path import sep

from plone.app.customerize import registration


class RegistrationsView(BrowserView):

    def getTemplateViewRegistrations(self):
        return registration.templateViewRegistrationGroups()

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
        url = sep.join(viewzpt.getPhysicalPath()) + "/manage_workspace"
        self.request.response.redirect(url)

