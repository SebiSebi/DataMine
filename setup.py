from setuptools import setup


# Read repository information. This will be used as the package description.
long_description = None
with open('README_PyPI.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
assert(long_description is not None)


requirements = [
        # 'TODO(sebisebi)': add
]

setup(
    name='data_mine',
    version='0.0.1',
    description='DataMine is a collection of datasets ready to be used for machine learning applications and not only.',  # noqa: E501
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='sebisebi',
    author_email='gpirtoaca@gmail.com',
    url='https://github.com/SebiSebi/DataMine',
    license='Apache 2.0',
    packages=[
        'data_mine',
    ],
    package_dir={'data_mine': 'data_mine'},
    install_requires=requirements,
    keywords='machine learning datasets data collection',
    classifiers=[
        'Development Status :: 1 - Planning',  # TODO(sebisebi): change.
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe=False,
)
