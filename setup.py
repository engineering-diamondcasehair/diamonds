from setuptools import setup

setup(
    name='DiamondCaseWeb',
    packages=['DiamondCaseWeb'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_assets',
        'flask-sqlalchemy'
    ],
)