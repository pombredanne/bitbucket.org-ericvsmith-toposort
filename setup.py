from __future__ import print_function
from distutils.core import setup, Command
import sys

# This is a hack in order to get the package name to be different when
#  building an RPM file. When 'setup.py bdist_rpm' is called, it invokes
#  setup.py twice more, with these command lines:
# ['setup.py', 'build']
# ['setup.py', 'install', '-O1', '--root=/home/eric/local/toposort/build/bdist.linux-i686/rpm/BUILDROOT/python-toposort-0.1-1.i386', '--record=INSTALLED_FILES']
# It's only on the original call (when bdist_rpm is in sys.argv) that
#  I adjust the package name. With Python 2.7, that's enough. I'm not
#  sure about 3.x.

name = 'toposort'
if 'bdist_rpm' in sys.argv:
    name = 'python{0}-{1}'.format('' if sys.version_info.major == 2 else '3', name)


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


setup(name=name,
      version='1.4',
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
                   ],
      license='Apache License Version 2.0',
      py_modules=['toposort'],

      cmdclass = {'test': PyTest},
      )
