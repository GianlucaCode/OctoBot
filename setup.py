from setuptools import setup

from config.cst import VERSION

DESCRIPTION = open('README.md').read() + '\n\n' + open('docs/CHANGELOG.md').read()

REQUIRED = open('requirements.txt').read()
REQUIRED_DEV = open('dev_requirements.txt').read()

setup(
    name='OctoBot',
    version=VERSION,
    packages=['backtesting', 'config', 'docs', 'evaluator', 'interfaces', 'services', 'tests', 'tools', 'trading'],
    url='https://github.com/Drakkar-Software/OctoBot',
    license='Apache-2.0',
    author='Trading-Bot team',
    description='Cryptocurrencies alert / trading bot',
    long_description=DESCRIPTION,
    entry_points={
        'console_scripts': [
            'start = start:main',
        ],
    },
    install_requires=REQUIRED,
    setup_requires=['pytest-runner'],
    tests_require=REQUIRED_DEV,
    test_suite="tests",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
