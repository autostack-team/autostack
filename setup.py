import setuptools
import subprocess

setuptools.setup(
    name="AutoStack",
    version="0.0.1",
    author="Elijah Sawyers, Benjamin Sanders, Caleb Werth",
    author_email="elijahsawyers@gmail.com, ben.sanders97@gmail.com, cwerth@crimson.ua.edu",
    description="Automatically detect python errors and search Stack Overflow.",
    url="https://github.com/elijahsawyers/AutoStack",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Mac OS",
    ],
)

subprocess.run(['./install.sh'])