from distutils.core import setup
from setuptools import find_packages

setup(
    name='unfuddle',
    version='0.1',
    author=u'Ryan Nagle',
    author_email='rmnagle@gmail.com',
    packages=find_packages('unfuddle'),
    url='http://github.com/newsapps/unfuddle-python',
    license='MIT, see LICENSE.md',
    description='Python wrapper for Unfuddle API',
    long_description=open('README.md').read(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'requests>=1.1.2',
    ]
)
