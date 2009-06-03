from setuptools import setup, find_packages

version = '1.1'

setup(name='archetypes.schemaextender',
      version=version,
      description="Dynamically extend Archetypes schemas with named adapters.",
      long_description=open("README.txt").read() + \
                        open("docs/INSTALL.txt").read() + \
                        open("docs/HISTORY.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        ],
      keywords='Archetypes Schema extend',
      author='Florian Schulze',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/archetypes.schemaextender',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['archetypes'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      )
