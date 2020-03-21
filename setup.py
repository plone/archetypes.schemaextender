from setuptools import setup, find_packages

version = '3.0.1'

setup(
    name='archetypes.schemaextender',
    version=version,
    description="Dynamically extend Archetypes schemas with named adapters.",
    long_description=(open("README.rst").read() + '\n' +
                      open("CHANGES.rst").read()),
    classifiers=[
        "Development Status :: 6 - Mature",
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: Core",
        "Framework :: Zope2",
        "Framework :: Zope :: 4",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Archetypes Schema extend',
    author='Florian Schulze',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://pypi.org/project/archetypes.schemaextender',
    license='GPL',
    packages=find_packages(),
    namespace_packages=['archetypes'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'six',
        'plone.uuid'
    ],
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
