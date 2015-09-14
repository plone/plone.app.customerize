Changelog
=========


1.3.2 (unreleased)
------------------

- Move tests to plone.app.testing.
  [bogdan.girman]

- Supress a ZopeTestCase warning.
  This fixes https://github.com/plone/Products.CMFPlone/issues/502
  [gforcada]


1.3.1 (2014-04-05)
------------------

- Attempt to fix test.
  [davisagli]


1.3.0 (2014-02-26)
------------------

- Remove DL from template.
  [khink]

- Make tests pass even with diazo.
  [davisagli]

- Upgrading test to adapt actual result on set difference.
  [bloodbar]


1.2.2 - 2011-02-25
------------------

- Add missing security declaration on the ViewTemplateContainer.
  [davisagli]


1.2.1 - 2010-10-27
------------------

- Fixed Chameleon incompatibility.
  [swampmonkey]

- Fix #11409 by storing the customized view name for future re-use
  [kiorky]


1.2 - 2010-07-18
----------------

- Update license to GPL version 2 only.
  [hannosch]


1.2b3 - 2010-06-13
------------------

- Moved ZCML registrations out of functional tests into a layer. This allows
  them to be torn-down correctly and avoids any registrations to end up in the
  local component registry.
  [hannosch]

- Move tests into tests sub-package and avoid some magic.
  [hannosch]


1.2b2 - 2010-06-03
------------------

- Update markup in customize.pt to facilitate usage as a popup form.
  [davisagli]


1.2b1 - 2009-12-01
------------------

- Change file format display format from
  `plone.app.customerize.tests/local.pt` to the full, absolute path name on
  the page detail view and tool tips.
  [MatthewWilkes]


1.2a1 - 2009-11-17
------------------

- Specified package dependencies and package metadata cleanup.
  [hannosch]

- Fixed test failures caused by changed HTML markup.
  [hannosch, davisagli]


1.1.2 - 2008-07-10
------------------

- Fixed a deprecation warning by using reg.factory instead of reg.value.
  [davisagli]

- Changed encoding of view registration requirements again, in order to
  properly support portlet renderer templates and fix issue #8275 which
  broke customerize in most cases.  Now *all* the requirements are used.
  [davisagli]


1.1.1 - 2008-07-07
------------------

- Re-enable browsertest introduced in r12928 after David's fix for the
  long-standing security issue (see #6196 and #8154)
  [witsch]

- Fixed request type lookup to use the second requirement for a view
  registration rather than the last.  This making it possible to
  customerize viewlet and portlet templates registered with the same
  name for multiple z3 browser layers.  See test introduced in r21154.
  [davisagli]


1.1 - 2008-04-20
----------------

- Fix problem with missing functions on test-layer.  See r20227.
  [ssh42]


1.0.3 - 2008-03-27
------------------

- Extension for browserlayer awareness.  For more details please see
  http://dev.plone.org/plone/ticket/7960
  [witsch]


1.0.2 - 2008-03-08
------------------

- Fix for a seemingly rare case of missing information about the zcml file
  a registration was made in.  See http://dev.plone.org/plone/ticket/7918
  [witsch]


1.0.1 - 2007-12-06
------------------

- Viewlet should be picked not only by name, but also by interface.
  Fixes http://dev.plone.org/plone/ticket/7408
  [witsch]


1.0 - 2007-08-17
----------------

- Support for viewlets and portlets, bug fixes
  [witsch]


1.0rc1 - 2007-07-08
-------------------

- Workaround for strange bug, where `absolute_url()` wouldn't return a full url,
  since `self.REQUEST` raised an `AttributeError`, even though `dir(self)`
  contains `REQUEST` at the time.
  Now `physicalPathToURL()` of the passed in request is used directly,
  just as it should have been via `absolute_url()`.
  [witsch]


1.0b3 - 2007-05-04
------------------

- No changes.


1.0b2 - 2007-04-30
------------------

- No changes.


1.0b1 - 2007-03-03
------------------

- ZMI views for customizing views, refactoring & cleanups
  [witsch]

- Initial version
  [witsch]

- Initial package structure.
  [witsch]
