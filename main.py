import csv, calendar, ast, glob
import shapely.geometry as sg
from shapely.geometry import Polygon, MultiPolygon
import matplotlib.pyplot as plt

from Perifereia import Perifereia
from Seismos import Seismos


PERIFEREIES_FILE = "perifereies.csv"
SEISMOI_PATH = "seismoi.dat"
PERIFEREIES_PATH = "data/regions"
regions = ['Π. ΑΝΑΤΟΛΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ - ΘΡΑΚΗΣ', 'Π. ΚΕΝΤΡΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ', 'Π. ΔΥΤΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ', 'Π. ΗΠΕΙΡΟΥ', 'Π. ΘΕΣΣΑΛΙΑΣ', 'Π. ΒΟΡΕΙΟΥ ΑΙΓΑΙΟΥ', 'Π. ΝΟΤΙΟΥ ΑΙΓΑΙΟΥ', 'Π. ΣΤΕΡΕΑΣ ΕΛΛΑΔΑΣ', 'Π. ΔΥΤΙΚΗΣ ΕΛΛΑΔΑΣ', 'Π. ΠΕΛΟΠΟΝΝΗΣΟΥ', 'Π. ΙΟΝΙΩΝ ΝΗΣΩΝ', 'Π. ΚΡΗΤΗΣ', 'Π. ΑΤΤΙΚΗΣ']
DESIRED_INDICES = [4, 12]
OUTPUT_PATH = "output/"
csv.field_size_limit(2**31-1)

# ena karo constants, enas theos kserei an xreiazontan kai ola


# lambda func gia na kanoume to asxhmo timestamp wraio mhna
get_month = lambda timestamp: calendar.month_name[int(timestamp[:2])]

'''
def get_month(timestamp):
    return calendar.month_name[int(timestamp[:2])]
'''


# operations gia na kanw dedomena twn csv objects
def findPolygons(polygons_data):
    if not polygons_data.strip():  # prostasia apo empty string input, w/e
        return []
    polygons = []
    # peta double quotes
    polygons_data = polygons_data.replace('"', '')
    # katharizoume 'MULTIPOLYGON ((' kai '))' apo arxh kai telos, spame to string me delimeters ta ')), ((' gia na skasei lista apo polygons
    polygons_data = polygons_data.replace('MULTIPOLYGON (((', '').rstrip('))').split(')), ((')
    for polygon_data in polygons_data:
        # delimeter to komma gia na paroume list of points
        points = polygon_data.split(', ')
        # kathe point anti gia komma anamesa se lat/lon exei keno, poly eksypno /s
        points = [tuple(map(float, point.split())) for point in points]
        polygons.append(tuple(points))
    return polygons


# apo to perifereies.csv pou phrame apo to kratos ftiaxnw Perifereia objects. gia kapoio logo to encoding='utf-8' einai aparaithto sta windows
# alliws den mporei na diavasei to arxeio
def loadPerifereies() -> list:
    perifereies = []
    with open(PERIFEREIES_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip to header
        for row in reader:
            FID, per, polygons_data = row
            polygons = findPolygons(polygons_data)  # dedicated function gia na kanei untagle ta multipolygon data, h kalyterh epilogh mou olo to 2024
            perifereies.append(Perifereia(FID, per, polygons))
    return perifereies

# kathe perifereia kai ena csv me to polygons ths
def serializePerifereies(perifereies):
    for i, perifereia in enumerate(perifereies):
        perifereia.file(i)

 
# pairnw ta region{index}.csv files kai ta kanw MultiPolygon objects, poly pio grhgora sth xrhsh apto na kanw iterate over every polygon
def readPolygonsFromFile(index):
    path = f"{PERIFEREIES_PATH}/region{index}.csv"
    polygons = []
    with open(path, 'r') as file:
        for line in file:
            # full voithitiko pou mporw na kanw interpret to ((float, float), (float,float)) ws tuple
            polygon_coordinates = ast.literal_eval(line.strip())
            # wraio class, den xreiasthke na to kanw egw
            polygons.append(Polygon(polygon_coordinates))
    # synthesi multipolygon, 2h kalyterh epilogh mou olo to 2024
    multipolygon = MultiPolygon(polygons)
    return multipolygon

"""
def findSeismoiPoints():
    # Create a list of MultiPolygon objects from the regional files
    multipolygons = [readPolygonsFromFile(i) for i in range(1, 14)]
    
    seismoi = openSeismoiFile()
    print("Latitude, Longitude, Magnitude, Month, Year, Perifereia")
    counter = 1
    for index, multipolygon in enumerate(multipolygons):
        string = "Latitude,Longitude,month,year,Magnitude\n"
        if index in desired_indices:
            for seismos in seismoi:
                if sg.Point(seismos.lon, seismos.lat).intersects(multipolygon):
                    _tmp = [str(item).rstrip() for item in seismos.prnt()]
                    if int(_tmp[4]) >= 1960 and int(_tmp[4]) <= 2010:
                        print(f"{_tmp[0]}, {_tmp[1]}, {_tmp[2]}, {get_month(_tmp[3])}, {_tmp[4]}, {regions[index]}")
                        string += f"{_tmp[0]}, {_tmp[1]}, {get_month(_tmp[3])}, {_tmp[4]}, {_tmp[2]}\n"
            with open(f"{output_path}output{counter}.csv", 'w') as f:
                f.write(string)
                counter += 1
"""

# to palio openSeismoiFile, apla unreadable
# to kainourgio einai eksisou unreadable alla toulaxiston einai 5 seires

def openSeismoiFile():
    with open(SEISMOI_PATH, 'r') as f:
        data = [tuple(line.split(" ")) for i, line in enumerate(f) if 17 < i < 11425]
        ref_data = [[entry for entry in lst if entry != ''] for lst in data]
        seismoi = [Seismos(year, dates, float(lat), float(lon), dep, M) for year, dates, lat, lon, dep, M in ref_data]
        return seismoi
    
def findSeismoiPoints():
    # kathe region file ftiaxnei kai ena multipolygon object
    # 100% mporw na to kanw poly pio memory efficient
    # alla ta data einai ligotera apo ton xrono pou menei opote den leei
    multipolygons = [readPolygonsFromFile(i) for i in range(1, 14)]
    
    # trexw kai checkarw gia kathe multipolygon (perifereia) poioi apo tous seismous eginan mesa tous. thewritika afou oi perioxes den exoun overlap
    # tha mporousame na tsekaroume o kathe seismso se poia apo tis 2 anhkei (an anoikei)
    # den xreiazetai, plus auto einai pio aplo sthn kataskevh twn strings
    seismoi = openSeismoiFile()
    print("Latitude, Longitude, Magnitude, Month, Year, Perifereia")
    counter = 1
    for index, multipolygon in enumerate(multipolygons):
        string = "Latitude,Longitude,month,year,Magnitude\n"
        if index in DESIRED_INDICES:
            for seismos in seismoi:
                if sg.Point(seismos.lon, seismos.lat).intersects(multipolygon):
                    _tmp = [str(item).rstrip() for item in seismos.prnt()]
                    if int(_tmp[4]) >= 1960 and int(_tmp[4]) <= 2010:
                        print(f"{_tmp[0]}, {_tmp[1]}, {_tmp[2]}, {get_month(_tmp[3])}, {_tmp[4]}, {regions[index]}")
                        string += f"{_tmp[0]}, {_tmp[1]}, {get_month(_tmp[3])}, {_tmp[4]}, {_tmp[2]}\n"
            with open(f"{OUTPUT_PATH}output{counter}.csv", 'w') as f:
                f.write(string)
                counter += 1

def visualizeData():
    plt.style.use('ggplot')  # ggwp

    earthquake_counts = {}
    region_names = ['Thessaly', 'Attica']

    for file in glob.glob(f"{OUTPUT_PATH}output*.csv"):
        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            decades = {}
            for row in reader:
                year = int(row['year'])
                decade = round(year / 10) * 10 
                if decade not in decades:
                    decades[decade] = 0
                decades[decade] += 1
            file_number = int(file.split('/')[-1].split('output')[1].split('.csv')[0]) -1 
            region_name = region_names[file_number]  
            earthquake_counts[region_name] = decades

    for region, counts in earthquake_counts.items():
        plt.figure()
        bars = plt.bar(counts.keys(), counts.values(), color='#003153', width=8)  # xontres mpares = wraies mpares
        # epishs prussian blue, #003153 aneta best color
        # dodgerblue poly dynatos contender https://matplotlib.org/stable/gallery/color/named_colors.html
        plt.title(f'Number of earthquakes per decade in {region}', pad=20)
        plt.xlabel('Decade', labelpad=15)
        plt.ylabel('Number of earthquakes', labelpad=15)
        plt.grid(True)

        # fainetai kalytero me ton arithmo epanw stis mpares
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, yval, ha='center', va='bottom')

        plt.show()

def main():
    # ftiaxnoume ta csv files
    serializePerifereies(loadPerifereies())

    # ta panta apo reading to seismoi.dat mexri na ftiaxnoume ta output files
    findSeismoiPoints()
    
    # visualize data, to wraio xalaro kommati. paizoume me xrwmatakia
    visualizeData()
    
    

if __name__ == "__main__":
    main()