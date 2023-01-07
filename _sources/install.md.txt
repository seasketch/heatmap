# Installation and Usage

A Docker recipe is available to install `heatmap` in an isolated virtual environment on your local computer with all dependencies.  In the future, a published module may be made available.

1. First install and start [Docker Desktop](https://www.docker.com/) on your local computer.  Windows, MacOS, Linux are all supported.

2. Clone the code, build a docker image, run a container with the image and open a shell to it, run final sap setup, then run the test suite to verify it's working:
```bash
    git clone https://github.com/seasketch/heatmap.git
```

3. Build docker image (only need to run once)
```bash
    cd heatmap
    docker-compose build heatmap
```

4. Start the container.
```bash
    docker-compose run --rm --service-ports heatmap
```
With this basic start command, the container only has access to the heatmap folder so any data inputs and outputs will need to be maintained within it.

5. Alternatively, start container with external folder mounts for input and output
```bash
docker-compose run --rm --service-ports -v /absolute/path/to/input:/work/input -v /absolute/path/to/output:/work/output  heatmap
```
With these volume mounts, config.json files can load shapes via `infile: '/work/input/my_shapes.shp`.  And `outpath: /work/output` can be used to write heatmaps back out of the container.

6. Optionally, verify everything installed correctly.
```bash
    pytest
```

## Example Projects

Multiple example projects are included that can be run out of the box.

`Simple` - small geographic extent.  Very simple test dataset with polygons that aligned to 100m boundaries for ease of interpreting the result.  Produces raster with 100m cell size.

`Maldives` - medium geographic extent.  Produces raster with 100m cell size.

`Canada` - large geographic extent. Demonstrates pushing the limits of raster file size and memory usage.  Produces raster with 400m cell size.

### Run the Simple project

```
cd examples/simple
gen_heatmap config.json
```

## Run the Canada project
You will need to generate random input data first.

```
cd examples/canada

../../scripts/gen_random_shapes config.json canada-poly.geojson

gen_heatmap config.json
```

## Creating a New Project

* Start the docker container with your input data (See #4 or #5 above).
* Start with copying any of the example folders
  * In config.json don't include a bounds parameter and it will default to the bounds of the input shapes.  But if you want to generate multiple rasters and maintain a consistent extent across each run you can choose an extent, for example using a tool like [Geofabrik provides]](https://tools.geofabrik.de/calc/#type=geofabrik_standard&tab=1&proj=EPSG:4326&places=2).
  * Default cell size of 100m is reasonable.

config.json file:
* There are two top-level properties: `runs` and `default`
* `default` contains the default options to pass to the genHeatmap() method for each run.  You can add/override all of the options accepted by the [genHeatmap](https://github.com/seasketch/heatmap/blob/main/lib/heatmap/gen_heatmap.py#L40>) method
* `runs` allows you to specify one or more runs (heatmaps) to generate.
  * Typically each run will have a different `infile`, this is because the output raster heatmap is always named the same as the infile, just with a `.tif` extension instead.  This is for ease of use, to limit the number of parameters you need to configure but it also limits how you can use the runs features. 
  * `infile` can point to any vector dataset supported by Fiona.  This could be shapefile, geojson, etc.

## Alternative Install (Work in progress)

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

Windows Option 1: Docker

Install and start Docker for Windows, then build and start a heatmap Docker image:

```
    git clone https://github.com/seasketch/heatmap.git
    cd heatmap
    docker-compose run --rm --service-ports heatmap
```
