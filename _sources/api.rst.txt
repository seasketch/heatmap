heatmap module
=============

.. automodule:: heatmap
    :members:


Methods
========

`genHeatmap() <https://github.com/seasketch/heatmap/blob/main/lib/heatmap/gen_heatmap.py#L40>`_
Follow link to view method options, all of which can be overriden from config.json

The genHeatmap methods works as follows:
* Open `infile` and make sure it contains features
* For each `infile` shape
 * If the shape is not valid, attempte to fix it, otherwise log it and move on
 * Calculate heat value depending on algorithm: sap, count, area.  Defaults to `sap`
 * Find shapes that may be smaller than a raster pixel and set them aside. They will be rasterized using the `ALL_TOUCHED` rasterize option.  All other shapes do not use this option because it seems to create some potentially incorrect artifacts/values in the raster
 * Rasterize the small shapes and the other shapes, and merge (add) the result
 * Write out the resulting raster to disk
 * Generate manifest and log files