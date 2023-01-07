from shapely.geometry import shape
import simplejson
from reprojectFeature import reprojectPolygon

def test_polygon_shape_reproject():
    polyShape4326 = shape({
        "type":"Polygon",
        "coordinates":[[[0, 0],[10, 0],[10, 10],[0, 10],[0,0]]]
    })

    # Reprojection of the above using QGIS as a source of truth
    polyShape3857 = shape({
        "type": "Polygon", 
        "coordinates": [ [ [ 0.0, 0.0 ], [ 1113194.907932735746726, 0.0 ], [ 1113194.907932735746726, 1118889.974857959430665 ], [ 0.0, 1118889.974857959430665 ], [ 0.0, 0.0 ] ] ]
    })

    # Web mercator to lat/lon
    reprojected = reprojectPolygon(polyShape3857, "epsg:3857", "epsg:4326")
    assert(simplejson.dumps(reprojected.__geo_interface__) == simplejson.dumps(polyShape4326.__geo_interface__))    

    # Then back
    original = reprojectPolygon(reprojected, "epsg:4326", "epsg:3857")
    jsonString = simplejson.dumps(original.__geo_interface__)
    checkString = simplejson.dumps(polyShape3857.__geo_interface__)
    
    # Should match the original
    assert(jsonString == checkString)

def test_multipolygon_shape_reproject():
    multipolyShape4326 = shape({
        "type":"MultiPolygon",
        "coordinates":[[[[0, 0],[10, 0],[10, 10],[0, 10],[0,0]]]]
    })

    # Reprojection of the above using QGIS as a source of truth
    multipolyShape3857 = shape({
        "type": "MultiPolygon", 
        "coordinates":[ [ [ [ 0.0, 0.0 ], [ 1113194.907932735746726, 0.0 ], [ 1113194.907932735746726, 1118889.974857959430665 ], [ 0.0, 1118889.974857959430665 ], [ 0.0, 0.0 ] ] ]]
    })

    # Web mercator to lat/lon
    reprojected = reprojectPolygon(multipolyShape3857, "epsg:3857", "epsg:4326")
    assert(simplejson.dumps(reprojected.__geo_interface__) == simplejson.dumps(multipolyShape4326.__geo_interface__))    

    # Then back
    original = reprojectPolygon(reprojected, "epsg:4326", "epsg:3857")
    jsonString = simplejson.dumps(original.__geo_interface__)
    checkString = simplejson.dumps(multipolyShape3857.__geo_interface__)
    
    # Should match the original
    assert(jsonString == checkString)

if __name__ == "__main__":
    test_polygon_shape_reproject()
    test_multipolygon_shape_reproject()