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

6. Optionally, verify everything installed correctly.  The container starts in `/projects`, so run the suite from the mounted repo:
```bash
    cd /work && pytest
```

### Apple Silicon / linux/arm64

The default image is linux/amd64 (`perrygeo/gdal-base` is not published for arm64). On an arm64 host, build and run the native image instead:

```bash
    docker compose --profile arm64 run --rm --service-ports heatmap-arm64
```

Or: `make shell-arm64`. The published runtime tag is `seasketch/heatmap:arm64`.

## Projects

The `projects/` directory is mounted into the container at `/projects` and is where your
own work lives.  Its contents are not tracked by git, so create one directory per project
with a `config.json` in it.

### Creating a New Project

* Start the docker container with your input data (See #4 or #5 above).
* Create a directory under `projects/` containing a `config.json`.
  * In config.json don't include a bounds parameter and it will default to the bounds of the input shapes.  But if you want to generate multiple rasters and maintain a consistent extent across each run you can choose an extent, for example using a tool like [Geofabrik provides]](https://tools.geofabrik.de/calc/#type=geofabrik_standard&tab=1&proj=EPSG:4326&places=2).
  * Default cell size of 100m is reasonable.

config.json file:
* There are two top-level properties: `runs` and `default`
* `default` contains the default options to pass to the genHeatmap() method for each run.  You can add/override all of the options accepted by the [genHeatmap](https://github.com/seasketch/heatmap/blob/main/lib/heatmap/gen_heatmap.py#L69>) method
* `runs` allows you to specify one or more runs (heatmaps) to generate.
  * Typically each run will have a different `infile`, this is because the output raster heatmap is always named the same as the infile, just with a `.tif` extension instead.  This is for ease of use, to limit the number of parameters you need to configure but it also limits how you can use the runs features. 
  * `infile` can point to any vector dataset supported by Fiona.  This could be shapefile, geojson, etc.

For example:

```json
{
    "default": {
        "outPath": "/projects/my-project/outputs",
        "outResolution": 100,
        "areaFactor": 1000000,
        "importanceField": "importance",
        "uniqueIdField": "shape_id",
        "allTouchedSmall": true,
        "overwrite": true
    },
    "runs": [
        { "infile": "/work/input/my_shapes.fgb" }
    ]
}
```

### Run a project

```
cd /projects/my-project
gen_heatmap config.json
```

Each run writes `{infile}.tif` to `outPath`, plus a `logs/` directory next to it holding
`{infile}.info.json` for every run.  Set `logToFile` to also write `{infile}.log.txt` and,
when features had to be skipped, `{infile}.error.geojson`.

### Generating the runs list

When a project has many input files, `update_runs` fills in the `runs` list from the
vector files in a directory rather than listing each one by hand.  It rewrites the `runs`
property of the config in place, leaving `default` untouched:

```
update_runs config.json /work/input
```

An optional glob restricts which files are picked up, and supports `**` for recursion:

```
update_runs config.json /work/input "sector-*.fgb"
```

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
