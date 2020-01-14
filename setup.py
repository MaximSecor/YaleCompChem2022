from setuptools import setup

setup(
    name = 'YaleCompChem',
    version = '0.1.0',
    description = "Submit scripts for Yale's computational chemistry course",
    author = 'jjgoings',
    long_description=open("README.md").read(),
    author_email = 'jjgoings@gmail.com',
    url = 'https://github.com/jjgoings/YaleCompChem',
    packages=['ycc'],
    include_package_data=True,
    install_requires=[
        # list of this package dependencies
    ],
    scripts=['bin/gausub'],
)
