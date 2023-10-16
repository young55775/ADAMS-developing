from setuptools import find_packages
from distutils.core import setup

install = ['numpy >= 1.17.2', 'opencv-python >= 4.7.0.12', 'scipy == 1.11.2', 'tqdm == 4.66.1', 'biopython == 1.81']


with open("Readme.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='adams',
    version='0.0.6',
    description='this is a program for fast protein structure search',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Guo_Zhengyang',
    author_email='guozy23@mails.tsinghua.edu.cn',
    install_requires=install,
    packages=find_packages(),
    license='GNU-GPL 3.0',
    classifiers=['Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', ],
    url='https://github.com/young55775/ADAMS-developing',
    include_package_data=True
)
