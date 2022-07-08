from setuptools import setup
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: zlib/libpng License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='bitskins',
  version='1.0.0',
  description='Simple BitSkins API Wrapper',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/Spacerulerwill/bitskins.py',  
  author='William Redding',
  author_email='williamdredding@gmail.com',
  license='zlib/libpng', 
  classifiers=classifiers,
  keywords='api', 
  packages=["bitskins"],
  install_requires=[''] 
)