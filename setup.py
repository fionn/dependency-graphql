"""Installation instructions"""
import setuptools
from pip._internal.req import parse_requirements

from src import name, __version__

with open("README.md", "r") as fh:
    # pylint: disable=invalid-name
    long_description = fh.read()

# pylint: disable=invalid-name
requirements = parse_requirements("requirements.txt", session="setup")

setuptools.setup(
    name=name,
    version=__version__,
    author="Fionn Fitzmaurice",
    description="Dependency graphs for GitHub repositories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fionn/dependency-graphql",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[str(req.req) for req in requirements],
    extras_require={"dev": ["pylint", "mypy"]},
    entry_points={"console_scripts": ["dependency-graphql = src.dependency_graphql:main"]},
    platforms=["Unix"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
    ],
)
