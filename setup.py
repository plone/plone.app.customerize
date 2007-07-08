from setuptools import setup, find_packages

setup(name = 'plone.app.customerize',
      version = '1.0rc1',
      description = 'Integrate five.customerize into Plone.',
      keywords = 'customerize plone five views page templates zmi',
      author = 'Plone Foundation',
      author_email = 'plone-developers@lists.sourceforge.net',
      url = 'http://svn.plone.org/svn/plone/plone.app.customerize/',
      download_url = 'http://cheeseshop.python.org/pypi/plone.app.customerize/',
      license = 'GPL',
      packages = find_packages(),
      namespace_packages = ['plone.app'],
      include_package_data = True,
      install_requires = ['setuptools',],
      platforms = 'Any',
      zip_safe = False,
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Zope2',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
      ],
      long_description = """\
        This package integrates five.customerize_ into Plone, which enables
        site administrators to customize five/zope3-style views TTW via the
        ZMI in a way similar to it's possible to customize filesystem-based
        skin elements via the portal skin "customize" procedure.
        
          .. _five.customerize: http://svn.zope.org/five.customerize/ """,
)

