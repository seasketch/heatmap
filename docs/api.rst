heatmap module
=============

.. automodule:: heatmap
    :members:


Methods
========

`genHeatmap() <https://github.com/seasketch/heatmap/blob/main/lib/heatmap/gen_heatmap.py#L69>`_
Follow link to view method options, all of which can be overriden from config.json

The genHeatmap methods works as follows:
* Open `infile` and make sure it contains features
* For each `infile` shape
 * If the shape is not valid, attempte to fix it, otherwise log it and move on
 * Find shapes that may be smaller than a raster pixel and set them aside. They will be rasterized using the `ALL_TOUCHED` rasterize option.  All other shapes do not use this option because it seems to create some potentially incorrect artifacts/values in the raster
 * Count how many output raster cells the shape covers, using the same `ALL_TOUCHED` setting it will be burned with
 * Calculate heat value depending on algorithm: sap, count, area.  Defaults to `sap`.  The `sap` and `area` methods divide by the shape's raster cell coverage (cell count multiplied by cell area) rather than by the area of the vector geometry
* Rasterize the small shapes and the other shapes into a single raster, adding their values
* Write out the resulting raster to disk
* Generate log and info files

Progress
========

`genHeatmap()` reports feature progress with a bar on stderr.  When it is called
directly it creates its own bar.  The `gen_heatmap` script instead counts the features
in every `infile` up front and passes one shared `FeatureProgress` to each run, so a
multi-run config reports progress across all of its files rather than restarting per file.

Output files
============

Alongside the `{infile}.tif` output raster, `genHeatmap()` writes a `logs/` directory
into the output directory containing:

* `{infile}.info.json` - the run manifest, including parameters, output dimensions and
  bounds, the included and excluded feature lists, and execution time.  Always written
* `{infile}.log.txt` - per-feature messages for fixed and skipped geometries.  Only
  written when `logToFile` is true, otherwise these are printed to stdout
* `{infile}.error.geojson` - the features that could not be used, as a FeatureCollection
  for inspection in GIS software.  Only written when `logToFile` is true and there were errors
