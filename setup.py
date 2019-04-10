from setuptools import setup

setup(
    name='pytest-taptest',
    description='Run tests which produce output in the TAP format',
    author='Oliver Sanders',
    author_email='oliver.sanders.email@googlemail.com',
    version='0.1',
    py_modules=['pytest_taptest'],
    entry_points={
        'pytest11': [
            'pytest_taptest = pytest_taptest',
        ]
    },
    install_requires=['py>=1.8.0'],
)
