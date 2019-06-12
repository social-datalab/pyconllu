import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pyconllu",
    version=read("VERSION"),
    author="Susana Sotelo",
    author_email="susana.sotelo@linguarum.net",
    description=(
        "Package with classes to manage files in CoNLL-U format."),
    license="GPL",
    packages=["pyconllu"],
    long_description=read("README.rst"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Topic :: Text Processing :: Linguistic",
    ]
)
