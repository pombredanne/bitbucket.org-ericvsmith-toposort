from __future__ import print_function
from setuptools import setup, Command

# run our tests
class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys, subprocess
        tests = [('test suite', ['-m', 'test.test_toposort']),
                 ]
        if sys.hexversion >= 0x03000000:
            # Skip doctests for python < 3.0. They use set literal reprs, which
            #  are different in 2.7. Testing under 3.x is good enough.
            tests.append(('doctests',   ['-m' 'doctest', 'README.txt']))
        for name, cmds in tests:
            print(name)
            errno = subprocess.call([sys.executable] + cmds)
            if errno != 0:
                raise SystemExit(errno)
        print('test complete')


setup(name='toposort',
      version='1.5',
      url='https://bitbucket.org/ericvsmith/toposort',
      author='Eric V. Smith',
      author_email='eric@trueblade.com',
      description='Implements a topological sort algorithm.',
      long_description=open('README.txt').read() + '\n' + open('CHANGES.txt').read(),
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   ],
      license='Apache License Version 2.0',
      py_modules=['toposort'],
      cmdclass = {'test': PyTest},
      )
