from setuptools import find_packages
from distutils.core import setup

install = ['numpy', 'opencv-python', 'scipy', 'tqdm', 'biopython']


with open("Readme.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='adams',
    version='0.0.11',
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
