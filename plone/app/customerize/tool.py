from five.customerize.interfaces import IViewTemplateContainer
from zope.interface import implements
from OFS.Folder import Folder

import registration
from layerfolder import LayerFolder

from plone.memoize import instance

class ViewTemplateContainer(Folder):
    """ a local utility storing all ttw view templates provided
        by five.customerize in a folder """
    implements(IViewTemplateContainer)

    id  = 'portal_view_customizations'
    title = 'Manages view customizations'
    meta_type = 'Plone View Customizations'

    manage_options = Folder.manage_options

    def addTemplate(self, id, template, layer):
        """ add the given ttw view template to the container """
        if isinstance(layer, str):
            layername = layer
        else:
            layername = registration.interfaceName(layer)
        layerfolder = self[layername]
        layerfolder._setObject(id, template)
        return getattr(layerfolder, id)

    @instance.memoize
    def _interfaces(self):
        regs = registration.templateViewRegistrations()
        info = registration.templateViewRegistrationInfos(regs)
        layers = dict((i['type'], i['typeiface']) for i in info)
        print "Got interfaces"
        return layers
    
    def _getFolders(self):
        i = self._interfaces()
        return dict(zip(i.keys(), [LayerFolder(iface) for iface in i.values()]))
    
    def __init__(self, *args, **kwargs):
        Folder.__init__(self, *args, **kwargs)
        for k,v in self._getFolders().items():
            self._setObject(k, v)