class Seismos():
    def __init__(self, year, dates, lat, lon, dep, M):
        self.year = year
        self.dates = dates
        self.lat = lat
        self.lon = lon
        self.dep = dep
        self.M = M
        
    def __str__(self):
        return(f"Year: {self.year}, Dates: {self.dates}, Lat: {self.lat}, Lon: {self.lon}, Dep: {self.dep}, M: {self.M}")