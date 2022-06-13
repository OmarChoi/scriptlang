from distutils.core import setup, Extension

module_spam = Extension('spam',
    sources=['spammodule.c'])

module_pyd = Extension('spam', 
    ['spam.pyd'])


setup(
    name='Running', 
    version='1.0',

    py_modules=['Running', 'APIConnect'],

    packages=['image', 'Telegram'],
    package_data = {'image': ['*.PNG'], 'Telegram' : ['*.py']},

    ext_modules=[module_spam, module_pyd]
)