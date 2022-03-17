from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="eaasi-uvi-client",
    description="Python client to get emulation environment recommendations from the EaaSI UVI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/artefactual-labs/eaasi-uvi-client",
    author="Artefactual Systems, Inc.",
    author_email="info@artefactual.com",
    license="Apache License 2.0",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["Click", "requests"],
    entry_points="""
        [console_scripts]
        get-eaasi-recommendations=cli.cli:get_recommendations
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
