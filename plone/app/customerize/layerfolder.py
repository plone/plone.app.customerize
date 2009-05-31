import Acquisition
from OFS.Folder import Folder
import registration

from plone.memoize import ram

from Products.CMFCore.FSPageTemplate import FSPageTemplate

def get_key(method, self):
    return ("cache_for_regs",)

class ViewFSPageTemplate(FSPageTemplate, Acquisition.Implicit):
    
    def __init__(self, id, viewname, filepath, required):
        FSPageTemplate.__init__(self, id, filepath)
        self.viewname = viewname
        self.required = required
    
    def listCustFolderPaths(self, type):
        v = self.portal_view_customizations.aq_inner._getFolders().keys()
        return zip(v,v)
    
    def manage_doCustomize(self, folder_path, RESPONSE=None):
        """Customise a template using pvc's magic"""
        pvc = self.portal_view_customizations.aq_inner
        path = "%s/@@customizezpt?required=%s&view_name=%s&layer=%s" % (
                    pvc.absolute_url(),
                    self.required,
                    self.viewname,
                    folder_path)
        return RESPONSE.redirect(path)


class LayerFolder(Folder):
    
    meta_type = 'Browser Layer'
    
    def __init__(self, Interface):
        self.interface = Interface
        Folder.__init__(self, registration.interfaceName(Interface))
    
    def objectIds(self, *args, **kwargs):
        print "Ids"
        a= self._objectDict().keys()
        print a

    def objectValues(self, *args, **kwargs):
        print "Values"
        return self._objectDict().values()
    
    def _originalObjectValues(self):
        return [self._getOb(id) for id in Folder.objectIds(self)]

    def _originalObjectIds(self):
        return Folder.objectIds(self)
    
    def _originalObjectItems(self):
        return zip(self._originalObjectIds(), self._originalObjectValues())
 
    def objectItems(self, *args, **kwargs):
        print "items"
        return self._objectDict().items()
    
    def _originalGetOb(self, name):
        return Folder._getOb(self, name, None)
    
    def _getOb(self, name, other=None):
        print "Getting ", name
        if name in self._originalObjectIds():
            return self._originalGetOb(name)
        else:
            try:
                return self._fakeObjectDict()[name]
            except:
                return self._originalGetOb(name)
    
    def _objectDict(self):
        a = self._fakeObjectDict()
        a.update(dict(self._originalObjectItems()))
        return a
    
    def _fakeObjectDict(self):
        # Combine the items that are really here with non-persistent
        # FS views
        return dict(self._fakeObjectItems())

    @ram.cache(get_key)
    def getRegs(self):
        regs = registration.templateViewRegistrations()
        infos = registration.templateViewRegistrationInfos(regs)
        return list(infos)
    
    def _fakeObjectItems(self):
        print "Getting registrations"
        infos = self.getRegs()
        infos = [a for a in infos if a['type'] == self.id]
        print "Filtered list for %s" % (infos[0]['type'])
        entries = []
        for info in infos:
            if info.get("abszptfile", None) is None:
                continue # We've customised this already
            id = registration.generateIdFromInfo(info)
            obj = ViewFSPageTemplate(id, info['viewname'], info['abszptfile'], info['required']).__of__(self)
            entries.append((id, obj))
        return tuple(entries)