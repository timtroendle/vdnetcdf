# VisiData NetCDF Loader

[![Build Status](https://travis-ci.org/timtroendle/vdnetcdf.svg)](https://travis-ci.org/timtroendle/vdnetcdf)

A VisiData plugin for reading NetCDF files.

## User Guide

Early prototype that let's you read NetCDF files within VisiData.

### Installation

Assuming you have `pip` and `Git` installed you can install the development version directly
from GitHub.

```bash
pip install git+git://github.com/timtroendle/vdnetcdf@develop
```

Then, update your VisiData config file by adding this line:

```Python
from vdnetcdf import open_nc
```

### Usage Example

```
vd some-data.nc
```

## Developer Guide

### Installation

Best install `vdnetcdf` in editable mode:

    $ pip install -r requirements-test.txt

Add `vdnetcdf` to your VisiData config, see above.

### Run the test suite

Run the test suite with py.test:

    $ py.test
