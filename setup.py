from setuptools import setup, find_packages

dependencies = ["requests>=2.22.0", "beautifulsoup4>=4.4.0"]


def read_version(module_name):
    from re import match, S
    from os.path import join, dirname

    f = open(join(dirname(__file__), module_name, "__init__.py"))
    return match(r".*__version__ = (\"|')(.*?)('|\")", f.read(), S).group(2)


setup(
    name="linkpreview",
    version=read_version("linkpreview"),
    description="Get link (URL) preview",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="MeyT",
    license="MIT",
    install_requires=dependencies,
    keywords="link preview web htmlparse schema.org opengraph twittercard url",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
    ],
    packages=find_packages(),
)
