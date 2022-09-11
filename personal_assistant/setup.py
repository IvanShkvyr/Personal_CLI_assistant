from setuptools import setup, find_packages

setup(name='personal_assistant',
      version='1.0.0',
      description='A personal assistant with a command line interface',
      url='https://github.com/IvanShkvyr/Personal_CLI_assistant',
      author='Ivan Shkvyr, Musfer Adzhymambetov, Taras Breurosh',
      author_email='GIS2011i@gmail.com',
      license='MIT',
      packages=find_packages(),
      entry_points={
                  'console_scripts': ['personal-assistant=personal_assistant.assistant:main',
                                          'clean-folder=personal_assistant.sort:main']
                  }
      )