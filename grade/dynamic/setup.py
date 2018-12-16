#!/usr/bin/env python

from setuptools import setup

packages = ['kutils', 'kutils.utils', 'kutils.parser']
package_dir = {'kutils': 'src',
               'kutils.utils': 'src/utils',
               'kutils.parser': 'src/parser'}

if __name__ == '__main__':

    setup(name='Kutils',
          version='0.01',
          description = 'Kodethon Utilities',
          author='Haochen Wu',
          author_email='kutils@haochenwu.com',
          packages=packages,
          package_dir=package_dir
    )
