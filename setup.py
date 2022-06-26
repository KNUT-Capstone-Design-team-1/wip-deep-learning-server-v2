import io
from setuptools import find_packages, setup

setup(
    name             = 'deeplearning-server',
    version          = '1.0',
    description      = 'extract features in pill image, for what_is_pill_app',
    author           = 'jintea519',
    author_email     = 'jintea519@gmail.com',
    url              = 'https://github.com/KNUT-Capstone-Design-team-1/new-what-is-pill/tree/main/deeplearning-server',
    install_requires = [],
    packages         = find_packages(),
    keywords         = ['pill', 'detection','recognition'],
    package_data     = {},
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.7'
)