from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='snmp-server',
    version='0.0.1',
    url='https://github.com/matheusphalves/snmp',
    license='MIT License',
    author= ['Matheus Phelipe','Murilo Stodolni', 'Nilton Vieira'],
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='matheusphalves@gmail.com',
    keywords=['Package', 'SNMP', 'Network', 'Sockets'],
    description=u'Basic SNMP Manager implementation for studies under networking purposes',
    packages=['snmp-server'],
    install_requires=['flask'],)