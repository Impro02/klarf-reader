from setuptools import setup

version = "0.4.3"

setup(
    name="klarf-reader",
    version=version,
    packages=[
        "klarf_reader",
        "klarf_reader.models",
        "klarf_reader.readers",
        "klarf_reader.utils",
    ],
    install_requires=["numba"],
    license="MIT",
    author="Maxime MARTIN",
    author_email="maxime.martin02@hotmail.fr",
    description="A project to parse klarf file and get klarf content as dataclass",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Impro02/klarf_reader",
    download_url="https://github.com/Impro02/klarf_reader/archive/refs/tags/%s.tar.gz"
    % version,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
