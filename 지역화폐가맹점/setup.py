from distutils.core import setup, Extension

module_spam = Extension('spam',
    sources=['spammodule.c'])

setup(
    name='Running', 
    version='1.0',

    py_modules=['Running', 'APIConnect'],

    packages=['image'],
    package_data = {'image': ['*.PNG']},

    ext_modules = module_spam
)