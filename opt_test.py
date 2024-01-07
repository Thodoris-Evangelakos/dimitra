import csv
import sys
from Perifereia import Perifereia
from Seismos import Seismos
import shapely.geometry as sg
from rtree import index

perifereies_path = "perifereies.csv"
seismoi_path = "seismoi.dat"
peloponnhsos_fid = "d7f50467-e5ef-49ac-a7ce-15df3e2ed738.9"
csv.field_size_limit(sys.maxsize)

def findPolygons(polygons_data):
    polygons = []
    # Remove double quotes
    polygons_data = polygons_data.replace('"', '')
    # Remove 'MULTIPOLYGON ((' and '))' from the start and end, and split by ')), ((' to get a list of polygons
    polygons_data = polygons_data.replace('MULTIPOLYGON (((', '').rstrip('))').split(')), ((')
    for polygon_data in polygons_data:
        # Split by ', ' to get a list of points
        points = polygon_data.split(', ')
        # For each point, split by space and convert the numbers to float
        points = [tuple(map(float, point.split())) for point in points]
        polygons.append(tuple(points))
    return polygons

def loadPerifereies() -> list:
    perifereies = [] 
    with open(perifereies_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header
        for row in reader:
            FID, per, polygons_data = row
            polygons = findPolygons(polygons_data)  # Pass the polygon data to findPolygons
            perifereies.append(Perifereia(FID, per, polygons))
    return perifereies

def openSeismoiFile():
    # too bulky, can be optimized but w.e
    with open(seismoi_path, 'r') as f:
        data = []
        for i, line in enumerate(f):
            if i > 19 and i < 11425:
                data.append(tuple(line.split(" ")))
        ref_data = []
        for lst in data:
            ref_data.append([entry for entry in lst if entry != ''])
        seismoi = []
        for item in ref_data:
            year, dates, lat, lon, dep, M = item
            seismoi.append(Seismos(year, dates, float(lat), float(lon), dep, M))
        return seismoi
    
def findSeismoiPoints():
    seismoi = openSeismoiFile()
    perifereies = loadPerifereies()

    # Create an R-tree index
    idx = index.Index()

    # Populate the index with each polygon's bounding box
    for i, perifereia in enumerate(perifereies):
        for polygon in perifereia.polygons:
            idx.insert(i, sg.Polygon(polygon).bounds)

    # For each seismos, find which polygon it's in
    for seismos in seismoi:
        point = sg.Point(seismos.lat, seismos.lon)
        print(f"Checking point {point}")
        intersections = list(idx.intersection((seismos.lat, seismos.lon)))
        print(f"Intersections: {intersections}")
        for j in intersections:
            for polygon in perifereies[j].polygons:
                poly = sg.Polygon(polygon)
                print(f"Checking polygon {poly}")
                if point.within(poly):
                    print(seismos)
                    print(perifereies[j])
                    print(polygon)
                    print()
                    
def test_findSeismoiPoints():
    # Create some test data
    seismoi = [Seismos(2000, "01-01", 1.0, 1.0, "10", "5.0")]
    perifereies = [Perifereia("1", "Test", [[(0.0, 0.0), (0.0, 2.0), (2.0, 2.0), (2.0, 0.0)]]), 
                   Perifereia("2", "Test2", [[(3.0, 3.0), (3.0, 5.0), (5.0, 5.0), (5.0, 3.0)]]),]

    # Create an R-tree index
    idx = index.Index()

    # Populate the index with each polygon's bounding box
    for i, perifereia in enumerate(perifereies):
        for polygon in perifereia.polygons:
            idx.insert(i, sg.Polygon(polygon).bounds)

    # For each seismos, find which polygon it's in
    for seismos in seismoi:
        point = sg.Point(seismos.lat, seismos.lon)
        print(f"Checking point {point}")
        intersections = list(idx.intersection((seismos.lat, seismos.lon)))
        print(f"Intersections: {intersections}")
        for j in intersections:
            for polygon in perifereies[j].polygons:
                poly = sg.Polygon(polygon)
                print(f"Checking polygon {poly}")
                if point.within(poly):
                    print(seismos)
                    print(perifereies[j])
                    print(polygon)
                    print()




def main():
    test_findSeismoiPoints()

if __name__ == "__main__":
    main()