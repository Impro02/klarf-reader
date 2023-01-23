from setuptools import setup

setup(
    name="klarf-reader",
    version="0.1.5",
    packages=["klarf_reader", "klarf_reader.models", "klarf_reader.readers"],
    install_requires=[
        "numpy",
    ],
    author="Maxime MARTIN",
    author_email="maxime.martin02@hotmail.fr",
    description="A project to parse klarf file and get klarf content as dataclass",
    url="https://github.com/Impro02/klarf_reader",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
