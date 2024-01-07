import re
import csv
import sys
import Perifereia

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
            perifereies.append(Perifereia.Perifereia(FID, per, polygons))
    return perifereies

def openSeismoiFile():
    with open(seismoi_path, 'r') as f:
        data = []
        for i, line in enumerate(f):
            if i > 19 and i < 11425:
                data.append(tuple(line.split(" ")))
        ref_data = []
        for lst in data:
            ref_data.append([entry for entry in lst if entry != ''])
        return ref_data


def main():
    #perifereies = loadPerifereies()
    data = openSeismoiFile()
    print(data)

if __name__ == "__main__":
    main()