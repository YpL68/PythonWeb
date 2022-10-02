from setuptools import setup, find_namespace_packages

setup(name='free_assist',
      version='1.0.3',
      description='Free Assistant',
      author='DreamTeam',
      author_email='test@example.com',
      license='MIT',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      packages=find_namespace_packages(),
      include_package_data=True,
      entry_points={'console_scripts': ['free-assist=free_assist.main:main']},
      install_requires=['python-dateutil', 'prompt-toolkit<=3.0.31']
      )