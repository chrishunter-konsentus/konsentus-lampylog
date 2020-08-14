import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="", # Replace with your own username
    version="0.0.1",
    author="Chris Hunter",
    author_email="chris.hunter@konsentus.com",
    description="A logger for Python Lambdas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrishunter-konsentus/konsentus-lampylog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
