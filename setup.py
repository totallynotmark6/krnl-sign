from setuptools import setup

setup(
    name='krnl_sign',
    version='0.0.1',    
    description='funny sign go brrrrrrrr',
    url='https://github.com/totallynotmark6/krnl-sign',
    author='Mark Smith',
    author_email='totallynotmark6@gmail.com',
    license='none',
    packages=['krnl_sign'],
    install_requires=['requests',
                      'arrow',
                      'segno'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
    ],
)