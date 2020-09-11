from setuptools import setup

install_requires = [
    'pytest'
]
tests_require = [
    'flake8',
    'pytest-tap'
]
extra_requires = {
    'all': tests_require
}


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
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extra_requires,
)
