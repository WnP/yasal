# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    with open('README.md', 'rb') as f:
        description = f.read()


setup(
    name='yasal',
    version='1.0.4',
    license='MIT',
    description='Yet another save as link',
    long_description=description,
    author='Steeve',
    author_email='mo0ofier@gmail.com',
    include_package_data=True,
    url='https://github.com/WnP/yasal',
    packages=find_packages(),
    install_requires=[
        'BeautifulSoup',
    ],
    entry_points={
        'console_scripts': [
            'yasal = yasal.yasal:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    zip_safe=False,
)
