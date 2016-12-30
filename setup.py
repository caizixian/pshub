# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pshub',

    version='0.0.1',

    description='A Pub/Sub framework implemented in Python',
    long_description=long_description,

    url='https://github.com/caizixian/pshub',

    author='Ivan Cai, lwher',
    author_email='caizixian@users.noreply.github.com, 751276936@qq.com',

    license='AGPLv3',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],

    keywords='asyncio pub sub',

    packages=find_packages(exclude=['examples', 'tests']),

    extras_require={
        'dev': ['pytest'],
        'test': ['pytest'],
    }
)
