from setuptools import setup
from setuptools import find_packages


setup(
    name='scrapeproxy',
    version='0.1.0',
    description='Dynamically scrape and use proxies from public sources',
    author='Data team',
    author_email='data@teamable.com',
    packages=find_packages(exclude=['tests']),
    install_requires=["requests==2.21.0", "bs4==0.0.1", "lxml","tqdm",
                      "pandas==0.24.2", "brotli==1.0.7", "selenium==3.141.0"],  # Optional
)
