from setuptools import setup, find_packages

setup(
    name='py_arris_exporter',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'bs4',
        'dogpile.cache'
    ],
    entry_points='''
        [console_scripts]
        py_arris_exporter=py_arris_exporter.main:main
    ''',
)
