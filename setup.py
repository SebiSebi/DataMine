from setuptools import find_packages, setup


# Read repository information. This will be used as the package description.
LONG_DESCRIPTION = None
with open('README_PyPI.md', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()
assert(LONG_DESCRIPTION is not None)


REQUIREMENTS = [
        # 'TODO(sebisebi)': add
]

setup(
    name='data_mine',
    version='0.0.5',
    description='DataMine is a collection of datasets ready to be used for machine learning applications and not only.',  # noqa: E501
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='sebisebi',
    author_email='gpirtoaca@gmail.com',
    url='https://github.com/SebiSebi/DataMine',
    license='Apache 2.0',
    packages=find_packages(),  # Anything with a __init__.py file.
    include_package_data=True,  # Includes the files in MANIFEST.in
    install_requires=REQUIREMENTS,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
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
