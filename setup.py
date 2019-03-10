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
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Software Development :: Quality Assurance',
      ],
      description='a CLI to format changed python from a git diff with `yapf`',
      entry_points={
          'console_scripts': ['yapf-diff = yapf_diff:run_main']
      },
      install_requires=['setuptools'],
      license='MIT',
      packages=['yapf_diff'],
      package_data={
          'yapf_diff': ['py.typed']
      },
      include_package_data=True,
      tests_require=['unittest'],
      url='https://github.com/luxresearch/yapf-diff',
      zip_safe=False)
