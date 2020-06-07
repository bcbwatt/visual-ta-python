from setuptools import setup

setup(
   name='pythonta',
   version='1.0',
   description='Technical analysis',
   author='Arjen van der Meulen',
   author_email='admin@avdmtech.com',
   packages=['pythonta'],  #same as name
   install_requires=['pandas', 'opencv-python', 'numpy'] #external packages as dependencies
)