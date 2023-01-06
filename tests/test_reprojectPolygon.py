from shapely.geometry import shape
import simplejson
from reprojectFeature import reprojectPolygon

polyShape = shape({
    "type":"Polygon",
    "coordinates":[[[0, 0],[0, 100],[200, 100],[200, 0],[0,0]]]
})

multipolyShape = shape({
    "type":"MultiPolygon",
    "coordinates":[[[[0, 0],[0, 100],[200, 100],[200, 0],[0,0]]]]
})

def test_polygon_shape_reproject():
    reprojected = reprojectPolygon(polyShape, "epsg:3857", "epsg:4326")
    original = reprojectPolygon(reprojected, "epsg:4326", "epsg:3857")
    jsonString = simplejson.dumps(original.__geo_interface__)
    checkString = '{"type": "Polygon", "coordinates": [[[0.0, 0.0], [0.0, 99.99999999999999], [199.99999999999997, 99.99999999999999], [199.99999999999997, 0.0], [0.0, 0.0]]]}'
    # Should be very very close to the original
    assert(jsonString == checkString)

def test_multipolygon_shape_reproject():
    reprojected = reprojectPolygon(multipolyShape, "epsg:3857", "epsg:4326")
    original = reprojectPolygon(reprojected, "epsg:4326", "epsg:3857")
    jsonString = simplejson.dumps(original.__geo_interface__)
    checkString = '{"type": "MultiPolygon", "coordinates": [[[[0.0, 0.0], [0.0, 99.99999999999999], [199.99999999999997, 99.99999999999999], [199.99999999999997, 0.0], [0.0, 0.0]]]]}'
    # Should be very very close to the original
    assert(jsonString == checkString)

if __name__ == "__main__":
    test_polygon_shape_reproject()
    test_multipolygon_shape_reproject()