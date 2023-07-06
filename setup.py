from setuptools import setup, find_packages

setup(
    name = 'bike-share-sim',
    version = '0.1.0',
    description = 'A simple Python simulation of a bike share such as Citi Bike',
    author = 'Marco Sanchez-Ayala',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    author_email = 'sanchezayala.marco@gmail.com',
    install_requires = [
        'numpy==1.18.2',
        'pytest==5.3.2',
        'pytest-mock==3.1.0',
        'scipy==1.10.0'
    ]
)