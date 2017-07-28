from distutils.core import setup

setup(
    name='Omission',
    version='1.0dev',
    author='MousePaw Games',
    author_email='info@mousepawgames.com',
    packages=['omission'],
    url='https://www.mousepawgames.com/omission',
    license='LICENSE.txt',
    description='A deceptively simple word puzzle.',
    install_requires=[
        'kivy >= 1.10.0',
        'appdirs >= 1.4.3',
    ],
)
