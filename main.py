import csv
import sys
import ast
from Perifereia import Perifereia
from Seismos import Seismos
import shapely.geometry as sg
from shapely.geometry import Polygon, MultiPolygon

perifereies_file = "perifereies.csv"
seismoi_path = "seismoi.dat"
peloponnhsos_fid = "d7f50467-e5ef-49ac-a7ce-15df3e2ed738.9"
perifereies_path = "data/regions"
csv.field_size_limit(sys.maxsize)

# read sum

def findPolygons(polygons_data):
    if not polygons_data.strip():  # Check if the input string is empty or contains only whitespace
        return []
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
    with open(perifereies_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header
        for row in reader:
            FID, per, polygons_data = row
            polygons = findPolygons(polygons_data)  # Pass the polygon data to findPolygons
            perifereies.append(Perifereia(FID, per, polygons))
    return perifereies

def serializePerifereies(perifereies):
    for i, perifereia in enumerate(perifereies):
        perifereia.file(i)

def readPolygonsFromFile(index):
    path = f"{perifereies_path}/region{index}.csv"
    polygons = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            for item in row:
                # Convert string representation of tuples to actual tuples
                polygon_coordinates = ast.literal_eval(item)
                # Create a Polygon object and append it to the list
                polygons.append(Polygon(polygon_coordinates))
    # Create a MultiPolygon object from the list of Polygon objects
    multipolygon = MultiPolygon(polygons)
    return multipolygon

def openSeismoiFile():
    # too bulky, can be optimized but w.e
    with open(seismoi_path, 'r') as f:
        data = []
        for i, line in enumerate(f):
            if i > 17 and i < 11425:
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
    for seismos in seismoi:
        for perifereia in perifereies:
            multipolygon = MultiPolygon(perifereia.polygons)
            if sg.Point(seismos.lat, seismos.lon).intersects(multipolygon):
                print(seismos)
                print(perifereia)
                print(multipolygon)
                print()


def main():
    # ftiaxnoume ta csv files
    serializePerifereies(loadPerifereies())
    

if __name__ == "__main__":
    main()