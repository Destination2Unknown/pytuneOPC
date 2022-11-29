from setuptools import setup, find_packages

setup(
    name='pytuneOPC',
    version='1.1.4',
    license='MIT',
    author="Destination2Unknown",
    author_email='destination0b10unknown@gmail.com',
    description='PID tuner, logger and simulator',
    long_description='PID tuner, logger and simulator, with multiple tuning methods',
    packages=find_packages(),
    url='https://github.com/Destination2Unknown/pytuneOPC',
    keywords='PID Tuner',
    classifiers= [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",        
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=[
          'scipy',
          'numpy',
          'matplotlib',
          'asyncua',
          'pandas',
      ],
)