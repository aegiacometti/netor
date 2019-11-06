import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fs:
    reqs = [r for r in fs.read().splitlines() if (len(r) > 0 and not r.startswith("#"))]

setuptools.setup(
    name="neto-aegiacometti",
    version="0.5",
    author="Adrian Giacometti",
    author_email="aegiacometti@hotmail.com",
    description="Network Orchestra",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aegiacometti/neto.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache License",
        "Operating System :: Linux",
    ],
    python_requires='>=3.6',
    install_requires=reqs,
)
