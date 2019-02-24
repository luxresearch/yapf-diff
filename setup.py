import sys

try:
    from setuptools import setup
except ImportError:
    print('`yapf-diff` needs setuptools in order to build. '
          'Install it using your package manager '
          '(usually python-setuptools) or via pip (pip install setuptools).')
    sys.exit(1)

setup(name='yapf-diff',
      version='0.0.1',
      author='Steven Kalt',
      author_email='kalt.steven@gmail.com',
      url='https://github.com/skalt/yapf-diff',
      description='a CLI to format changed python from a git diff with `yapf`',
      license='MIT',
      install_requires=['setuptools'],
      tests_require=['unittest'],
      packages=['flask_webpack'],
      zip_safe=False,
      data_files=[])
