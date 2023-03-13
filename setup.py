from setuptools import find_packages, setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='self-hosted-bible',
    version='1.0.0',
    description="A self-hosted webapp of various Bible versions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samhaswon/selfhosted-bible",
    author="Samuel Howard",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'requests',
        'multipledispatch',
        'requests-cache',
        'flask-bootstrap',
        'flask-wtf',
        'wtforms',
        'waitress',
    ],
)
