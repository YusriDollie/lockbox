from distutils.core import setup

setup(
    name='lockbox',
    version='0.1dev',
    packages=['lock_box',],
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=[
        'pytest',
        'cryptography',
        'pycrypto',
        'arrow',
        # linters and type checkers
        'prospector',
        'mypy',
        'mock',
    ],
)
