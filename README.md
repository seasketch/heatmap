
# sapmap

![sapmap package](https://github.com/seasketch/python-sap-map/actions/workflows/test-sapmap.yml/badge.svg)

`sapmap` takes the areas that a group identifies as important and combines them into a map of `spatial access priorities (SAP)`

![example polygon](docs/img/survey-sap-start-end.png)

This aggregate map is used in area-based planning exercises for identifying where important areas exist and measuring the impact if changes in access are made.

Common questions it can answer include:
```
Which geographic areas are important to the group?  The most important?  The least important?

Is area A of more value to the group than area B?  How much more?

If the use of a given area is changed, will people be impacted?  How much of the groups value is within this area?
```

## Notable Publications

Yates KL, Schoeman DS (2013) Spatial Access Priority Mapping (SAPM) with Fishers: A Quantitative GIS Method for Participatory Planning. PLoS ONE 8(7): e68424. [https://doi.org/10.1371/journal.pone.0068424](https://doi.org/10.1371/journal.pone.0068424)

Klein CJ, Steinback C, Watts M, Scholz AJ, Possingham HP (2010) Spatial marine zoning for fisheries and conservation. Frontiers in Ecology and the Environment 8: 349–353. Available: [https://doi.org/10.1890/090047](https://doi.org/10.1890/090047)


## Debugging
The `examples` folder includes samples to get you started.  
Debug examples and tests within VSCode.  debupy starts in container listening on port, waits for vscode

```
    cd examples/simple
    python -m debugpy --listen 0.0.0.0:5678 --wait-for-client simple_sap_map.py
```

or

```
    cd tests
    python -m debugpy --listen 0.0.0.0:5678 --wait-for-client test_simple_sap_map.py
```

In VSCode, set a breakpoint, Click `Debug` in the left menu, then click `Python Attach`.  It will attach to the debugpy port and then execute the script

## Alternative Install

### Install and run in OSX

Install pipenv to your user home directory:

```
    pip3 install --user pipenv
```

Add user base binary directory to your PATH

```
    /Users/twelch/Library/Python/3.9/bin
```

```
    pip3 install numpy
    pip3 install --no-binary fiona rasterio shapely
```

### Install and run in Windows

* Install VS Code - https://code.visualstudio.com/Download
* Install python 3 from Windows Store if possible, otherwise use python.org.  If you use python.org be sure to 'add Python to my path' and turn off execution aliases for Python (or else it will try to open the windows store every time you run python
* Open terminal and run GitBash terminal

```
    & 'C:\Program Files\Git\bin\bash.exe'
```

Windows Option 1: Docker

Install and start Docker for Windows, then build and start a sapmap Docker image:

```
    git clone https://github.com/seasketch/python-sap-map.git
    cd python-sap-map
    docker-compose build debug # not necessary?
    docker-compose run --rm --service-ports sapmap
```

Windows Option 2: Python virtual environment

```
    pip install virtualenv
    virtualenv env-sapmap
    source env-sapmap/Scripts/activate
    pip install --upgrade pip
```

Follow the rasterio windows instructions - https://rasterio.readthedocs.io/en/latest/installation.html#windows
Pointed to install GDAL and Rasterio wheels from https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal.  Look for the latest win_amd64:

```
    pip install .\GDAL-3.3.1-cp39-cp39-win_amd64.whl
    pip install .\rasterio-1.2.6-cp39-cp39-win_amd64.whl
    pip install -r requirements.txt
    pip install -r requirements_dev.txt
```

deactivate the virtual Python environment when done, activate again when needed, or delete

```
    deactivate
```
