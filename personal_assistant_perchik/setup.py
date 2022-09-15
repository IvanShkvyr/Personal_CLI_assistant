from setuptools import setup, find_packages

setup(name='personal_assistant_perchik',
      version='1.0.2',
      description='A personal assistant with a command line interface',
      url='https://github.com/IvanShkvyr/Personal_CLI_assistant',
      author='Ivan Shkvyr, Musfer Adzhymambetov, Taras Breurosh',
      author_email='GIS2011i@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['InquirerPy>=0.3.0','keyboard'],
      entry_points={
                  'console_scripts': ['personal-assistant=personal_assistant_perchik.assistant:main',
                                          'clean-folder=personal_assistant_perchik.sort:main']
                  }
      )
