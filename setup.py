import setuptools

__version__ = "0.0.1"

with open("./README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="active-toml-config",
    version="0.0.1",
    author="Clayton Bezuidenhout",
    author_email="claytonbez.nl@gmail.com",
    description="A small package to assist in loading and parsing toml config as env dict.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/claytonbez/active-toml-config",
    project_urls={
        "Bug Tracker": "https://github.com/claytonbez/active-toml-config/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=("tests", "dist", "sdist")),
    install_requires=["pytoml"],
    python_requires=">=3.8",
)