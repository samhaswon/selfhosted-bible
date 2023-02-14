from setuptools import find_packages, setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='esv-web',
    version='1.0.0',
    description="A self-hosted webapp connecting to Crossway's ESV API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samhaswon/ESV-web",
    author="Samuel Howard",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'requests',
        'pymongo',
        'multipledispatch',
        'requests-cache',
        'flask-bootstrap',
        'flask-wtf',
        'wtforms',
        'waitress',
    ],
)
