from setuptools import setup, find_packages

setup(
    name='cadastro',
    version='0.1.0',
    author='Erik Marques',
    maintainer='erikmarques',
    email='lucro.alternativo@otlook.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
        'openpyxl',
        'pytest',
        'pytest-cov',
        'pytest-mock',
        'selenium',
        'webdriver_manager',
    ],
)