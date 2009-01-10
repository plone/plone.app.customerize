from setuptools import setup, find_packages
from os.path import join

name = 'plone.app.customerize'
path = name.split('.') + ['version.txt']
version = open(join(*path)).read().strip()
readme = open("README.txt").read()
history = open(join('docs', 'HISTORY.txt')).read().replace(name + ' - ', '')

setup(name = name,
      version = version,
      description = 'Integrate five.customerize into Plone.',
      long_description = readme[readme.find('\n\n'):] + '\n' + history,
      keywords = 'customerize plone five views page templates zmi',
      author = 'Plone Foundation',
      author_email = 'plone-developers@lists.sourceforge.net',
      url = 'http://pypi.python.org/pypi/plone.app.customerize/',
      license = 'GPL',
      packages = find_packages(),
      namespace_packages = ['plone', 'plone.app'],
      include_package_data = True,
      extras_require=dict(
          test=[
            'plone.app.layout',
            'zope.testing',
            'Products.PloneTestCase',
          ]
      ),
      install_requires = [
        'setuptools',
        'five.customerize',
        'plone.browserlayer',
        'plone.portlets',
        'zope.component',
        'zope.interface',
        'zope.publisher',
        'zope.viewlet',
        'Products.CMFCore',
        # 'Acquisition',
        # 'Zope2',
      ],
      platforms = 'Any',
      zip_safe = False,
      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Zope2',
        'Framework :: Zope3',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
      ],
)

