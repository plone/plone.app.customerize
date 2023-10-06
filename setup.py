from pathlib import Path
from setuptools import find_packages
from setuptools import setup


version = "2.0.1"

long_description = (
    f"{Path('README.rst').read_text()}\n{Path('CHANGES.rst').read_text()}"
)

setup(
    name="plone.app.customerize",
    version=version,
    description="Integrate five.customerize into Plone.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "Framework :: Zope :: 5",
        "Intended Audience :: Other Audience",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
    ],
    keywords="customerize plone views page templates zmi",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://pypi.org/project/plone.app.customerize/",
    license="GPL version 2",
    packages=find_packages(),
    namespace_packages=["plone", "plone.app"],
    include_package_data=True,
    python_requires=">=3.8",
    extras_require=dict(
        test=[
            "Products.GenericSetup",
            "plone.app.layout",
            "plone.app.testing",
            "plone.testing",
        ]
    ),
    install_requires=[
        "setuptools",
        "five.customerize",
        "plone.browserlayer",
        "plone.portlets",
        "zope.component",
        "zope.interface",
        "zope.publisher",
        "zope.viewlet",
        "Products.CMFCore",
        "Acquisition",
    ],
    platforms="Any",
    zip_safe=False,
)
