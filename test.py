import csv
import sys

csv.field_size_limit(sys.maxsize)
data = "perifereies.csv"

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

# Open the data file
with open(data, 'r') as f:
    reader = csv.reader(f)
    # Skip the header row
    next(reader)
    # Read each row
    for row in reader:
        # Split the row by commas to separate the id, name, and polygons data
        id, name, polygons_data = row
        # Use the findPolygons function to extract the coordinates from the polygons data
        polygons = findPolygons(polygons_data)
        # Print the polygons
        for polygon in polygons:
            for point in polygon:
                print(point)