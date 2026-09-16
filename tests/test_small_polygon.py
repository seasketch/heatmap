from heatmap import genHeatMap
import os.path
import rasterio
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
resolution = 100
pixelArea = resolution * resolution

def test_small_polygon_lost():
    infile = os.path.join(DATA, 'off-center-polygon.geojson')
    outfile = os.path.join(DATA, 'off-center-polygon.tif')

    assert(os.path.isfile(infile))
    manifest = genHeatMap(
        infile,
        outResolution=resolution,
        bounds=[-100, -100, 100, 100],
        areaFactor=pixelArea,
        overwrite=True
    )
    # assert(os.path.isfile(outfile))
    assert(len(manifest['included']) == 1)

    with rasterio.open(outfile) as reader:
        assert(manifest['outBounds'][0] == reader.bounds.left)
        assert(manifest['outBounds'][1] == reader.bounds.bottom)
        assert(manifest['outBounds'][2] == reader.bounds.right)
        assert(manifest['outBounds'][3] == reader.bounds.top)
        
        assert(manifest['height'] == reader.height == 2)
        assert(manifest['width'] == reader.width == 2)
        assert(manifest['params']['outResolution'] == reader.res[0] == reader.res[1])
        assert(reader.nodata == 0.0)

        arr = reader.read()
        # Bresenham centerline algorithm will miss the small polygon and get zero
        assert(np.all((arr == 0)))

def test_small_polygon_found():
    infile = os.path.join(DATA, 'off-center-polygon.geojson')
    outfile = os.path.join(DATA, 'off-center-polygon.tif')

    assert(os.path.isfile(infile))
    manifest = genHeatMap(
        infile,
        outResolution=resolution,
        bounds=[-100, -100, 100, 100],
        areaFactor=pixelArea,
        allTouchedSmall=True,
        overwrite=True
    )
    assert(os.path.isfile(outfile))
    assert(len(manifest['included']) == 1)

    with rasterio.open(outfile) as reader:
        assert(manifest['outBounds'][0] == reader.bounds.left)
        assert(manifest['outBounds'][1] == reader.bounds.bottom)
        assert(manifest['outBounds'][2] == reader.bounds.right)
        assert(manifest['outBounds'][3] == reader.bounds.top)
        
        assert(manifest['height'] == reader.height == 2)
        assert(manifest['width'] == reader.width == 2)
        assert(manifest['params']['outResolution'] == reader.res[0] == reader.res[1])
        assert(reader.nodata == 0.0)

        arr = reader.read()
        # should pick up polygon smaller than pixel resolution
        # Area is the one cell it all-touches, so heat is 1 / (pixelArea / areaFactor) = 1
        checkArr = np.array([[
            [0,  1],
            [0, 0],
        ]], dtype=np.float32)

        np.testing.assert_array_equal(arr, checkArr)

def test_area_floor_does_not_change_small_classification():
    """areaFloor lowers the heat value but must not affect which shapes are treated as small

    Small shapes are classified from the vector shape index alone, which areaFloor
    does not touch, so the polygon is still all-touched into the same single cell.
    """
    infile = os.path.join(DATA, 'off-center-polygon.geojson')
    outfile = os.path.join(DATA, 'off-center-polygon.tif')

    assert(os.path.isfile(infile))
    manifest = genHeatMap(
        infile,
        outResolution=resolution,
        bounds=[-100, -100, 100, 100],
        areaFactor=pixelArea,
        areaFloor=1000000,
        allTouchedSmall=True,
        overwrite=True
    )
    # Still classified small, so it still lands in the same cell as test_small_polygon_found
    assert(manifest['includedSmallCount'] == 1)

    with rasterio.open(outfile) as reader:
        arr = reader.read()
        # Cell area of 10,000m^2 is raised to the 1,000,000m^2 floor before areaFactor
        # 1 importance / (1,000,000 / 10,000) = 0.01
        checkArr = np.array([[
            [0, 0.01],
            [0, 0],
        ]], dtype=np.float32)

        np.testing.assert_array_equal(arr, checkArr)

# Used for debugging
if __name__ == "__main__":
    test_small_polygon_lost()
    test_small_polygon_found()
    test_area_floor_does_not_change_small_classification()