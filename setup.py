import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="safer_totp",
    version="0.0.1",
    author="Example Author",
    author_email="asaf400@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["mintotp==0.3.0","tinydb==4.5.2","pypiwin32", "SecretStorage==3.3.1",'docopt', 'tabulate'],
    # url="https://github.com/pypa/sampleproject",
    # project_urls={
    #     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points='''
    [console_scripts]
    yourscript=yourscript:cli
    '''
)