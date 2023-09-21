import setuptools
install = ['numpy >= 1.17.2','opencv-python >= 4.7.0.12','scipy == 1.11.2','tqdm == 4.66.1','biopython == 1.81']
setup = ['numpy','scipy','opencv-python','tqdm','pickle','biopython']


import setuptools
setuptools.setup(
    name='dia',
    version='1.0',
    description='this is a program for dia',
    author='Guo Zhengyang',
    author_email='guozy23@mails.tsinghua.edu.cn',
	setup_requires=setup,
	install_requires=install,
    packages=setuptools.find_packages(),
   )
