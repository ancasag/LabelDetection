#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages, Command
from sys import platform as _platform
from shutil import rmtree
import sys
import os

here = os.path.abspath(os.path.dirname(__file__))
NAME = 'labelDetection'
REQUIRES_PYTHON = '>=3.0.0'
REQUIRED_DEP = ['pyqt5', 'lxml','clodsa==1.2.37','setuptools==40.6.2','gluoncv==0.5.0','tensorflow==1.14.0','imutils==0.5.1','tqdm==4.31.0','opencv_python==4.1.2.30','XlsxWriter==1.2.6','six==1.11.0','matplotlib==3.0.3','Keras==2.1.6','Keras-Applications==1.0.6','Keras-Preprocessing==1.0.5','keras-resnet==0.1.0',
'keras-retinanet==0.5.1','numpy','Pillow==7.0.0','mxnet==1.5.0','progressbar2==3.47.0','sip==4.19.8','scikit_learn==0.22.1','future==0.17.1','pandas==0.23.4','imageio==2.5.0','scikit-image==0.14.2']
about = {}

with open(os.path.join(here, 'libs', '__init__.py')) as f:
    exec(f.read(), about)

readme = ""
#with open('README.md') as readme_file:
#    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


# OS specific settings
SET_REQUIRES = []
if _platform == "linux" or _platform == "linux2":
   # linux
   print('linux')
elif _platform == "darwin":
   # MAC OS X
   SET_REQUIRES.append('py2app')

required_packages = find_packages()
required_packages.append('labelDetection')
required_packages.append('ensemble')
required_packages.append('EfficientDet')
required_packages.append('kerasfcos')
required_packages.append('FSAF')
required_packages.append('FSAF/augmentor')
required_packages.append('FSAF/generators')
required_packages.append('FSAF/models')
required_packages.append('FSAF/utils')
required_packages.append('FSAF/yolo')
required_packages.append('mrcnn')
required_packages.append('notebooks')
required_packages.append('predict')

APP = [NAME + '.py']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'resources/icons/app.icns'
}

class UploadCommand(Command):
    """Support setup.py upload."""

    description=readme + '\n\n' + history,

    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            self.status('Fail to remove previous builds..')
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system(
            '{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag -d v{0}'.format(about['__version__']))
        os.system('git tag v{0}'.format(about['__version__']))
        # os.system('git push --tags')

        sys.exit()


setup(
    app=APP,
    name=NAME,
    version="0.1.1",
    description="LabelDetection is a graphical tool for using and creating detection models",
    long_description=readme + '\n\n' + history,
    author="Angela Casado",
    author_email='angela.casado@unirioja.es',
    url='https://github.com/ancasag/labelDetection',
    python_requires=REQUIRES_PYTHON,
    package_dir={'labelDetection': '.'},
    packages=required_packages,
    entry_points={
        'console_scripts': [
            'labelDetection=labelDetection.labelDetection:main'
        ]
    },
    include_package_data=True,
    install_requires=REQUIRED_DEP,
    license="MIT license",
    zip_safe=False,
    keywords='labelDetection detection deeplearning',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    package_data={'data/predefined_classes.txt': ['data/predefined_classes.txt'],'notebooks': ['notebooks/*.ipynb']},
    options={'py2app': OPTIONS},
    setup_requires=SET_REQUIRES,
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    }
)
