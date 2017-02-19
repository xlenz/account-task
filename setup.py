from distutils.core import setup
from setuptools.config import read_configuration

conf_dict = read_configuration('setup.cfg')

setup(name='accountModule',
      version='0.0.1',
      description='Account',
      long_description='command line accounting tool',
      url='https://github.com/mgrybyk/accountModule-task',
      author='Mykola Grybyk',
      author_email='mykola.grybyk@gmail.com',
      packages=['accountModule'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest']
      )
