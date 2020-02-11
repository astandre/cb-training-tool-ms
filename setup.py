import sys
from setuptools import setup, find_packages
from kbsbot.training_tool import __version__

setup(name='training_tool',
      description="",
      long_description=open('README.rst').read(),
      version=__version__,
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      dependency_links=["https://github.com/Runnerly/flakon.git#egg=flakon"],
      install_requires=["flask", "flask_sqlalchemy", "rdflib", "pymongo", "rdflib-jsonld", "flask_cors"],
      author="André Herrera",
      author_ewmail="andreherrera97@hotmail.com",
      license="MIT",
      keywords=["microservices"],
      entry_points={
          'console_scripts': [
              'training_tool = kbsbot.training_tool.run:app',
          ],
      }
      )
