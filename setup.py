# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '1.3.10'

setup(
    name='plone.app.customerize',
    version=version,
    description='Integrate five.customerize into Plone.',
    long_description=open('README.rst').read() + '\n' +
    open('CHANGES.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Framework :: Plone :: 5.2',
        'Framework :: Zope2',
        'Framework :: Zope :: 4',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
    keywords='customerize plone views page templates zmi',
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://pypi.org/project/plone.app.customerize/',
    license='GPL version 2',
    packages=find_packages(),
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    extras_require=dict(
        test=[
            'plone.app.layout',
            'plone.app.testing',
            'six',
            'zope.testing',
        ]
    ),
    install_requires=[
        'setuptools',
        'five.customerize',
        'plone.browserlayer',
        'plone.portlets',
        'zope.component',
        'zope.interface',
        'zope.publisher',
        'zope.viewlet',
        'Products.CMFCore',
        'Acquisition',
        'Zope2',
    ],
    platforms='Any',
    zip_safe=False,
)
