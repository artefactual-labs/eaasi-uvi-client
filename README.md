# eaasi-uvi-client

## About

Python client for getting emulation environment recommendations from
the [EaaSI](eaasi) software platform's Universal Virtual Interactor, or
UVI.

## Usage

### Command-line interface

After installing package with `pip`, use `get-eaasi-recommendations`:

```
Usage: get-eaasi-recommendations [OPTIONS]

  Get emulation environment suggestions from EaaSI API.

Options:
  --eaasi-url TEXT  EaaSI host URL.  [required]
  --data-url TEXT   Data URL for content to characterize.  [required]
  --data-type TEXT  Data type. Allowed values: "zip", "tar", "bagit+zip",
                    "bagit+tar"  [default: zip]
  --help            Show this message and exit.

```

### Python library

The `eaasi_uvi_client` Python library consists mainly of the
`EaaSIUVIClient` class, which has the following public methods:

* `EaaSIUVIClient.get_recommendations()`: returns dictionary
	representation of the JSON returned by EaaSI's EnvironmentProposer
	API endpoints; raises `requests.ConnectionError` or
	`eaasi_uvi_client.ResultNotFound` on error.
* `EaaSIUVIClient.parse_suggested_environments()`: returns list of
	dictionaries with suggested emulation environments from JSON
	returned by EaaSI's EnvironmentProposer API endpoints; raises
	`eaasi_uvi_client.ResultNotFound` if `get_recommendations()` has not
	yet been called.

See `cli/cli.py` for an implementation example.

## Installation

### Install eaasi_uvi_client package

`eaasi-uvi-client` requires Python 3.6+.

#### Via PyPI

```bash
pip install eaasi-uvi-client
```

#### Manually

Download this repo:

```bash
git clone https://github.com/artefactual-labs/eaasi-uvi-client.git
```

Change into the cloned directory and install:

```bash
cd eaasi-uvi-client/
pip install .
```

## Development

### Installation

For development, it may be useful to install `eaasi-uvi-client` with
`pip install -e .`, which will apply changes made to the source code
immediately.


### Publishing to PyPI

This repository contains a [Makefile](Makefile) with commands to aid in
building packages and publishing to [PyPI][pypi].

To check that the package is valid:
```bash
make package-check
```

To upload the package to PyPI (this requires PyPI credentials and being
listed as a collaborator on the `auditmatica` project):
```bash
make package-upload
```

To clean up package distribution files:
```bash
make clean
```

[eaasi]: https://www.softwarepreservationnetwork.org/emulation-as-a-service-infrastructure/
