from setuptools import setup, find_packages

setup(
    name="klarf-reader",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
    ],
    author="Maxime MARTIN",
    author_email="maxime.martin02@hotmail.fr",
    description="A project to parse klarf file and get klarf content as dataclass",
    url="https://github.com/Impro02/klarf-reader",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
