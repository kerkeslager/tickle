import pathlib
from setuptools import setup, find_packages
HERE = pathlib.Path(__file__).parent
VERSION = '0.0.5'
PACKAGE_NAME = 'django_predrill_tickle'
AUTHOR = 'David Kerkeslager'
AUTHOR_EMAIL = 'david@kerkeslager.com'
URL = 'https://github.com/kerkeslager/tickle'
LICENSE = 'AGPL3.0'
DESCRIPTION = 'A pluggable Django app for keeping rock climbing ticklists'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"
INSTALL_REQUIRES = [
      'Django',
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    license=LICENSE,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,
    packages=['tickle'],
)
