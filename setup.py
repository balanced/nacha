import re
import setuptools


version = (
    re
    .compile(r".*__version__ = '(.*?)'", re.S)
    .match(open('nacha/__init__.py').read())
    .group(1)
)

packages = setuptools.find_packages('.', exclude=('tests', 'tests.*'))

install_requires = [
]

extras_require = {
    'tests': [
        'nose >=1.0,<2.0',
    ],
}

setuptools.setup(
    name='nacha',
    version=(
        re
        .compile(r".*__version__ = '(.*?)'", re.S)
        .match(open('nacha/__init__.py').read())
        .group(1)
    ),
    url='https://github.com/bninja/nacha',
    author='Egon Spengler',
    author_email='egon+nacha@gb.com',
    description='',
    long_description='',
    platforms='any',
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=extras_require['tests'],
    packages=packages,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='nose.collector',
)
