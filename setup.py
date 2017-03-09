from setuptools import setup, find_packages

version = '2.1.7'

setup(
    name='archetypes.schemaextender',
    version=version,
    description="Dynamically extend Archetypes schemas with named adapters.",
    long_description=(open("README.rst").read() + '\n' +
                      open("CHANGES.rst").read()),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Archetypes Schema extend',
    author='Florian Schulze',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://pypi.python.org/pypi/archetypes.schemaextender',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['archetypes'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.uuid'
    ],
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)