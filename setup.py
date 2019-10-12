import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arcade",
    version="0.0.3",
    author="Yábir Benchakhtir",
    author_email="yabirg@protonmail.com",
    description="A static blog generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yabirgb/arcade",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    py_modules=["arcade.main"],
    install_requires=[
        'click==7.0',
        'jinja2==2.10.3',
        'livereload==2.6.1',
        'markdown==3.1.1',
        'markupsafe==1.1.1',
        'pygments==2.4.2',
        'pyyaml==5.1.2',
        'six==1.12.0',
        'tornado==6.0.3',
    ],
    entry_points={
        "console_scripts" : [
            "arcade=arcade.main:cli"
        ]
    },
    include_package_data=True
)
